from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Create a unique hash value using native Python 3 strings.
        If user ID, timestamp, or active status changes, the token breaks.
        """
        return (
            str(user.pk) + 
            str(timestamp) + 
            str(user.is_active)
        )

# Instantiate the token generator object
account_activation_token = AccountActivationTokenGenerator()