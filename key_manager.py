"""
API Key Manager with Automatic Fallback
Handles API key switching when one fails or quota exceeds
"""

from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import time
from typing import List, Optional

from config.logging_config import api_logger
from config.settings import settings


class KeyManager:
    """Manages API keys with automatic fallback"""

    def __init__(self):
        """Initialize key manager"""
        self.api_keys: List[str] = settings.API_KEYS
        self.current_key_index: int = 0
        self.key_failure_log: dict = {}
        self.key_usage_log: dict = {}
        self.log_file: Path = settings.LOGS_DIR / "key_switching.log"

        if not self.api_keys:
            api_logger.error("No API keys found in .env file")
            raise ValueError("At least one API key is required in .env file")

        api_logger.info(
            f"KeyManager initialized with {len(self.api_keys)} API keys"
        )

        self.load_failure_log()

    def get_current_key(self) -> str:
        """Get current active API key"""
        if self.current_key_index >= len(self.api_keys):
            self.current_key_index = 0

        return self.api_keys[self.current_key_index]

    def switch_key(self, reason: str = "Unknown") -> str:
        """Switch to next available API key"""
        old_index = self.current_key_index

        # Advance pointer
        self.current_key_index = (self.current_key_index + 1) % len(
            self.api_keys
        )
        new_key = self.get_current_key()

        switch_info = {
            "timestamp": datetime.now().isoformat(),
            "from_key_index": old_index,
            "to_key_index": self.current_key_index,
            "reason": reason,
        }

        api_logger.warning(
            f"API Key switched from index {old_index} to {self.current_key_index}. Reason: {reason}"
        )
        api_logger.debug(f"Switch details: {json.dumps(switch_info, indent=2)}")

        self._log_key_switch(switch_info)
        self._mark_key_failure(key_index=old_index)

        return new_key

    def mark_key_failed(self, reason: str = "Unknown error") -> str:
        """
        Mark current key as failed and switch to next

        Args:
            reason: Reason for failure

        Returns:
            New API key
        """
        api_logger.error(f"API Key failed: {reason}")

        return self.switch_key(reason=f"Failure: {reason}")

    def mark_key_success(self):
        """Mark current key as successfully used"""
        key_index = self.current_key_index

        if key_index not in self.key_usage_log:
            self.key_usage_log[key_index] = {
                "count": 0,
                "last_used": None,
                "failures": 0,
                "successes": 0,
            }

        self.key_usage_log[key_index]["count"] += 1
        self.key_usage_log[key_index]["last_used"] = (
            datetime.now().isoformat()
        )
        self.key_usage_log[key_index]["successes"] += 1

    def _mark_key_failure(self, key_index: int = None):
        """Mark specific key index as failed"""
        if key_index is None:
            key_index = self.current_key_index

        if key_index not in self.key_failure_log:
            self.key_failure_log[key_index] = {
                "failures": 0,
                "last_failure": None,
                "failure_reasons": [],
            }

        self.key_failure_log[key_index]["failures"] += 1
        self.key_failure_log[key_index]["last_failure"] = (
            datetime.now().isoformat()
        )

    def _log_key_switch(self, switch_info: dict):
        """Log key switch to file"""
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(switch_info) + "\n")
        except Exception as e:
            api_logger.error(f"Failed to log key switch: {e}")

    def load_failure_log(self):
        """Load previous failure log from file"""
        if self.log_file.exists():
            try:
                with open(self.log_file, "r") as f:
                    for line in f:
                        if line.strip():
                            log_entry = json.loads(line)
                            key_index = log_entry.get("to_key_index")

                            if key_index not in self.key_failure_log:
                                self.key_failure_log[key_index] = {
                                    "failures": 0,
                                    "last_failure": None,
                                }

                            self.key_failure_log[key_index]["last_failure"] = (
                                log_entry.get("timestamp")
                            )

                api_logger.info("Previous key failure log loaded")
            except Exception as e:
                api_logger.error(f"Failed to load failure log: {e}")

    def get_key_status(self) -> dict:
        """Get status of all keys"""
        status = {
            "total_keys": len(self.api_keys),
            "current_key_index": self.current_key_index,
            "usage_log": self.key_usage_log,
            "failure_log": self.key_failure_log,
        }
        return status

    def rotate_key_strategy(self) -> str:
        """
        Rotate to healthiest key (least failures)

        Returns:
            Best available key
        """

        best_key_index = 0
        min_failures = float("inf")

        for key_index in range(len(self.api_keys)):
            failures = self.key_failure_log.get(key_index, {}).get(
                "failures", 0
            )

            if failures < min_failures:
                min_failures = failures
                best_key_index = key_index

        if best_key_index != self.current_key_index:
            self.current_key_index = best_key_index
            api_logger.info(
                f"Rotated to healthier key at index {best_key_index}"
            )

        return self.get_current_key()

    def validate_all_keys(self) -> List[bool]:
        """
        Validate all API keys (basic check)

        Returns:
            List of validation results
        """
        results = []
        for key in self.api_keys:
            is_valid = bool(key) and len(key) > 20
            results.append(is_valid)

        valid_count = sum(results)
        api_logger.info(
            f"Key validation: {valid_count}/{len(self.api_keys)} keys valid"
        )

        return results


_key_manager: Optional[KeyManager] = None


def get_key_manager() -> KeyManager:
    """Get or create key manager instance"""
    global _key_manager

    if _key_manager is None:
        _key_manager = KeyManager()

    return _key_manager


def get_current_api_key() -> str:
    """Get current API key"""
    return get_key_manager().get_current_key()


def switch_api_key(reason: str = "Unknown") -> str:
    """Switch to next API key"""
    return get_key_manager().switch_key(reason=reason)


def mark_api_key_failed(reason: str = "Unknown error") -> str:
    """Mark current key as failed and get new one"""
    return get_key_manager().mark_key_failed(reason=reason)


def mark_api_key_success():
    """Mark current key as successful"""
    get_key_manager().mark_key_success()