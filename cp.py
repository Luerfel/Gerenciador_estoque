import numpy as np

class HillCipher:
    def __init__(self, key_matrix):
        # Inicializa a cifra de Hill com a matriz chave fornecida
        self.key_matrix = np.array(key_matrix)  # Converte a matriz chave em um array numpy
        self.modulus = 26  # Define o módulo como 26 (número de letras no alfabeto)
        self.matrix_size = self.key_matrix.shape[0]  # Obtém o tamanho da matriz chave
        
        # Verifica se a matriz chave é invertível no módulo 26
        if not self.is_invertible():
            raise ValueError("The key matrix is not invertible under modulo 26.")
        
        # Calcula a matriz inversa no módulo 26
        self.inverse_key_matrix = self.find_inverse_matrix()

    def is_invertible(self):
        # Calcula o determinante da matriz chave e verifica se ele tem inverso multiplicativo no módulo 26
        det = int(np.round(np.linalg.det(self.key_matrix))) % self.modulus
        return np.gcd(det, self.modulus) == 1  # Verifica se o MDC do determinante e do módulo é 1

    def find_inverse_matrix(self):
        # Calcula o determinante da matriz chave
        det = int(np.round(np.linalg.det(self.key_matrix))) % self.modulus
        
        # Calcula o inverso multiplicativo do determinante no módulo 26
        det_inv = pow(det, -1, self.modulus)
        
        # Calcula a matriz adjunta (adjugate) da matriz chave
        adjugate = np.round(np.linalg.det(self.key_matrix) * np.linalg.inv(self.key_matrix)).astype(int) % self.modulus
        
        # Calcula a matriz inversa no módulo 26
        inverse_matrix = (det_inv * adjugate) % self.modulus
        return inverse_matrix

    def preprocess_text(self, text):
        # Converte para letras maiúsculas e armazena posições dos espaços
        text = text.upper()
        text_with_spaces = [(i, char) for i, char in enumerate(text) if char == ' ']  # Salva as posições dos espaços
        text = ''.join([char for char in text if char.isalpha()])  # Remove caracteres não alfabéticos
        return text, text_with_spaces

    def reinsert_spaces(self, text, spaces):
        # Reinsere os espaços nas posições originais
        for index, _ in spaces:
            text = text[:index] + ' ' + text[index:]
        return text

    def encrypt(self, plaintext):
        # Preprocessa o texto claro para remover caracteres não alfabéticos e armazena espaços
        plaintext, spaces = self.preprocess_text(plaintext)
        
        # Converte cada letra do texto claro para um número (A=0, B=1, ..., Z=25)
        plaintext_numbers = [ord(char) - ord('A') for char in plaintext]
        
        # Adiciona 'X' ao final do texto claro se o tamanho não for múltiplo do tamanho da matriz chave
        while len(plaintext_numbers) % self.matrix_size != 0:
            plaintext_numbers.append(ord('X') - ord('A'))
        
        # Converte a lista de números para uma matriz
        plaintext_matrix = np.array(plaintext_numbers).reshape(-1, self.matrix_size)
        
        # Multiplica a matriz de texto claro pela matriz chave e aplica o módulo 26
        encrypted_matrix = (plaintext_matrix @ self.key_matrix) % self.modulus
        
        # Converte a matriz cifrada de volta para texto
        ciphertext = ''.join(chr(num + ord('A')) for num in encrypted_matrix.flatten())
        
        # Reinsere os espaços nas posições originais
        ciphertext = self.reinsert_spaces(ciphertext, spaces)
        return ciphertext

    def decrypt(self, ciphertext):
        # Preprocessa o texto cifrado para remover caracteres não alfabéticos e armazena espaços
        ciphertext, spaces = self.preprocess_text(ciphertext)
        
        # Converte cada letra do texto cifrado para um número (A=0, B=1, ..., Z=25)
        ciphertext_numbers = [ord(char) - ord('A') for char in ciphertext]
        
        # Converte a lista de números para uma matriz
        ciphertext_matrix = np.array(ciphertext_numbers).reshape(-1, self.matrix_size)
        
        # Multiplica a matriz cifrada pela matriz inversa e aplica o módulo 26
        decrypted_matrix = (ciphertext_matrix @ self.inverse_key_matrix) % self.modulus
        
        # Converte a matriz de texto claro de volta para texto
        plaintext = ''.join(chr(num + ord('A')) for num in decrypted_matrix.flatten())
        
        # Remove o padding 'X' adicionado durante a criptografia
        plaintext = plaintext.rstrip('X')
        
        # Reinsere os espaços nas posições originais
        plaintext = self.reinsert_spaces(plaintext, spaces)
        return plaintext

"""
# Exemplo de uso
key_matrix_2x2 = [
    [3, 3],
    [2, 5]
]

cipher = HillCipher(key_matrix_2x2)

# Testando criptografia e descriptografia
plaintext = "HELLO world"
ciphertext = cipher.encrypt(plaintext)
print(f"Ciphertext: {ciphertext}")

decrypted_text = cipher.decrypt(ciphertext)
print(f"Decrypted text: {decrypted_text}")
"""
