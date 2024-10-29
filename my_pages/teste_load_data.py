import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


from Load_data_categorie_date import load_data  

class TestLoadDataProduct(unittest.TestCase):

    @patch('load_data.pymysql.connect')
    def test_load_data_product(self, mock_connect):
        # Mock de la connexion et du curseur
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Définir les retours pour le curseur et la connexion
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'idProduit': 125, 'nom': 'Produit 125', 'prix': 9.99},
            {'idProduit': 126, 'nom': 'Produit 126', 'prix': 12.99}
        ]
        
        # Appeler la fonction
        df = load_data_product(125)
        
        # Vérifier que la requête est exécutée correctement
        mock_cursor.execute.assert_called_once_with("SELECT * FROM produit WHERE idProduit = %s", (125,))
        
        # Vérifier que le DataFrame est correctement formaté
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)  # Vérifier le nombre de lignes
        self.assertIn('idProduit', df.columns)  # Vérifier que la colonne existe
        self.assertEqual(df.iloc[0]['nom'], 'Produit 125')  # Vérifier la valeur d'une colonne
    
    # Test avec un produit non trouvé
    @patch('votre_module.pymysql.connect')
    def test_load_data_product_no_result(self, mock_connect):
        # Mock connexion et curseur sans résultats
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        # Appeler la fonction avec un ID de produit inexistant
        df = load_data_product(999)

        # Vérifier que le DataFrame est vide
        self.assertTrue(df.empty)
        
if __name__ == '__main__':
    unittest.main()
