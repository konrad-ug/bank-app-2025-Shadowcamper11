import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.account import Account, Company_Account


class TestEmailHistory:
    
    @pytest.fixture
    def personal_account(self):
        return Account("John", "Doe", "12345678911")
    
    @pytest.fixture
    @patch('src.account.requests.get')
    def company_account(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        mock_get.return_value = mock_response
        return Company_Account("Test Corp", "8461627563")
    
    @patch('src.account.SMTPClient')
    def test_personal_account_send_email_success(self, mock_smtp_class, personal_account):
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        personal_account.incoming_transfer(100)
        
        result = personal_account.send_history_via_email("test@example.com")
        
        assert result is True
        mock_smtp_instance.send.assert_called_once()
        
        call_args = mock_smtp_instance.send.call_args[0]
        today = datetime.now().strftime('%Y-%m-%d')
        assert call_args[0] == f"Account Transfer History {today}"
        assert "Personal account history:" in call_args[1]
        assert call_args[2] == "test@example.com"
    
    @patch('src.account.SMTPClient')
    def test_personal_account_send_email_failure(self, mock_smtp_class, personal_account):
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        result = personal_account.send_history_via_email("test@example.com")
        
        assert result is False
        mock_smtp_instance.send.assert_called_once()
    
    @patch('src.account.SMTPClient')
    def test_company_account_send_email_success(self, mock_smtp_class, company_account):
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        company_account.incoming_transfer(5000)
        
        result = company_account.send_history_via_email("company@example.com")
        
        assert result is True
        call_args = mock_smtp_instance.send.call_args[0]
        assert "Company account history:" in call_args[1]
    
    @patch('src.account.SMTPClient')
    def test_company_account_send_email_failure(self, mock_smtp_class, company_account):
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        result = company_account.send_history_via_email("company@example.com")
        
        assert result is False
