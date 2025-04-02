import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import re

# Descargar recursos de NLTK si aún no están disponibles
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Configurar lematizador y stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    """
    Preprocesa texto aplicando limpieza, tokenización, eliminación de nombres propios,
    eliminación de stopwords y lematización.

    Parameters
    ----------
    text : str
        Texto que se desea procesar.

    Returns
    -------
    str
        Texto limpio y procesado.

    Ejemplo de uso:
    ---------------
        preprocess_text("This is an Example text! Proper nouns and stopwords should be removed.") -> "example text proper noun remove"
    """
    if not isinstance(text, str):
        raise ValueError("El parámetro 'text' debe ser de tipo str.")

    # Eliminar caracteres no alfabéticos y espacios redundantes
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenizar el texto
    tokens = word_tokenize(text)

    # Etiquetar las palabras y eliminar nombres propios
    tokens = [word for word, tag in pos_tag(tokens) if tag not in ['NNP', 'NNPS']]

    # Convertir a minúsculas y eliminar stopwords
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Lematizar las palabras
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Combinar tokens en una cadena de texto procesada
    return ' '.join(tokens)