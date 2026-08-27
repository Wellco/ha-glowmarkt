"""Tests for integration setup behaviour."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.glowmarkt as integration
from custom_components.glowmarkt.const import DOMAIN
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import CoreState
from homeassistant.exceptions import ConfigEntryAuthFailed

from tests.fakes import FakeGlowClient
from tests.fakes import http_error


async def test_async_setup_entry_raises_auth_failed_for_stored_credentials(
    hass,
) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"username": "user@example.com", "password": "secret"},
    )

    with patch.object(
        integration,
        "GlowClient",
        side_effect=http_error(401, "Unauthorized"),
    ):
        with pytest.raises(ConfigEntryAuthFailed):
            await integration.async_setup_entry(hass, entry)


async def test_async_setup_entry_defers_history_loop_until_hass_is_running(
    hass,
) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"username": "user@example.com", "password": "secret"},
    )
    entry.add_to_hass(hass)
    hass.state = CoreState.starting

    background_task = object()

    def fake_create_background_task(hass_arg, target, name, eager_start=True):
        assert hass_arg is hass
        assert name == "glowmarkt_history_statistics"
        assert eager_start is False
        target.close()
        return background_task

    with (
        patch.object(
            integration,
            "GlowClient",
            return_value=FakeGlowClient([]),
        ),
        patch.object(
            hass.config_entries,
            "async_forward_entry_setups",
            AsyncMock(return_value=True),
        ),
        patch.object(
            entry,
            "async_create_background_task",
            side_effect=fake_create_background_task,
        ) as mock_create_background_task,
        patch.object(hass, "async_create_task") as mock_create_task,
    ):
        assert await integration.async_setup_entry(hass, entry) is True
        assert hass.data[DOMAIN][entry.entry_id]["history_task"] is None
        mock_create_background_task.assert_not_called()

        hass.state = CoreState.running
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)
        await hass.async_block_till_done()

        assert hass.data[DOMAIN][entry.entry_id]["history_task"] is background_task
        mock_create_background_task.assert_called_once()
        mock_create_task.assert_not_called()
