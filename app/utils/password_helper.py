from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHelper:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify if a plain password matches a hashed password.
        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to compare against.
        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate a hash of the given password.
        Args:
            password (str): The password to be hashed.
        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)
