import pytest
from unittest.mock import MagicMock, patch
import importlib
import sys

@pytest.fixture
def mock_engine_machine():
    mock_sm = MagicMock()
    # Default behavior for check_transition
    mock_sm.check_transition.return_value = (True, "mocked")
    # Default behavior for get_valid_transitions
    mock_sm.get_valid_transitions.return_value = []
    
    with patch.dict('sys.modules', {
        'organvm_engine.governance.state_machine': mock_sm
    }):
        import src.promotion
        # Reload to ensure the mocked module is picked up
        importlib.reload(src.promotion)
        try:
            yield mock_sm
        finally:
            # Reload again after the patch to restore original state for other tests
            importlib.reload(src.promotion)

class TestEngineStateMachine:
    def test_engine_allowed_exact_match(self, mock_engine_machine):
        import src.promotion
        mock_engine_machine.check_transition.return_value = (True, "mock message")
        
        # Test states that map exactly to themselves (if any) or when canonical matches legacy
        # In this implementation, current_canonical == current and target_canonical == target
        assert src.promotion._engine_allowed("UNKNOWN", "UNKNOWN2") is True
        mock_engine_machine.check_transition.assert_called_with("UNKNOWN", "UNKNOWN2")
        
    def test_engine_allowed_exact_match_false(self, mock_engine_machine):
        import src.promotion
        mock_engine_machine.check_transition.return_value = (False, "mock message")
        
        assert src.promotion._engine_allowed("UNKNOWN", "UNKNOWN2") is False

    def test_engine_allowed_via_valid_transitions(self, mock_engine_machine):
        import src.promotion
        # Check transition will be skipped because canonical != current
        # e.g., PLANNED -> INCUBATOR
        mock_engine_machine.get_valid_transitions.return_value = ["LOCAL", "CANDIDATE"]
        
        # SKELETON maps to LOCAL
        assert src.promotion._engine_allowed("PLANNED", "SKELETON") is True
        mock_engine_machine.get_valid_transitions.assert_called_with("INCUBATOR")

    def test_engine_allowed_archived_unarchive(self, mock_engine_machine):
        import src.promotion
        mock_engine_machine.get_valid_transitions.return_value = []
        
        # This should return True because of the specific ARCHIVED -> PRODUCTION check
        assert src.promotion._engine_allowed("ARCHIVED", "PRODUCTION") is True

    def test_engine_allowed_fails(self, mock_engine_machine):
        import src.promotion
        mock_engine_machine.get_valid_transitions.return_value = []
        
        # Should fall through and return False
        assert src.promotion._engine_allowed("PLANNED", "PRODUCTION") is False
        
    def test_can_promote_with_engine(self, mock_engine_machine):
        import src.promotion
        
        # If legacy fails but engine succeeds
        mock_engine_machine.get_valid_transitions.return_value = ["CANDIDATE"]
        # "PLANNED" -> "PROTOTYPE" is legacy invalid.
        # "PROTOTYPE" canonical is "CANDIDATE", which we allow here.
        assert src.promotion.can_promote("PLANNED", "PROTOTYPE") is True
        
    def test_can_promote_invalid_state(self, mock_engine_machine):
        import src.promotion
        
        # Test invalid states fall out early
        assert src.promotion.can_promote("INVALID_STATE", "SKELETON") is False
        assert src.promotion.can_promote("PLANNED", "INVALID_STATE") is False

    def test_promote_with_engine_not_allowed(self, mock_engine_machine):
        import src.promotion
        
        # Need a current state that has NO VALID_TRANSITIONS locally so that 
        # _HAS_ENGINE_STATE_MACHINE and not allowed evaluates to True.
        
        # Actually, let's create a temporary new state that has no valid transitions.
        src.promotion.ALL_STATES.add("NO_TRANS_STATE")
        try:
            mock_engine_machine.get_valid_transitions.return_value = ["ALLOWED_CANONICAL"]
            
            result = src.promotion.promote("NO_TRANS_STATE", "PRODUCTION", "test-repo")
            assert result.success is False
            assert "Cannot promote" in result.message
            # Should include canonical allowed options from engine
            assert "ALLOWED_CANONICAL" in result.message
        finally:
            # Clean up
            src.promotion.ALL_STATES.remove("NO_TRANS_STATE")
