from passlib.context import CryptContext


class Hasher:
	pwd_context = CryptContext(schemes=["bcrypt"])

	@staticmethod
	def verify_password(plain_password, hashed_password):
		return Hasher.pwd_context.verify(plain_password, hashed_password)

	@staticmethod
	def get_hashed_password(plain_password):
		return Hasher.pwd_context.hash(plain_password)
