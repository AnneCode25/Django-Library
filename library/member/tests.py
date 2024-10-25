from django.test import TestCase
from django.urls import reverse
from shared_models.models import Book, DVD, CD, BoardGame


class MemberViewsTest(TestCase):
    def setUp(self):
        # Créer des médias pour les tests
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            is_available=True
        )
        self.dvd = DVD.objects.create(
            title="Test DVD",
            director="Test Director",
            is_available=True
        )
        self.cd = CD.objects.create(
            title="Test CD",
            artist="Test Artist",
            is_available=True
        )
        self.boardgame = BoardGame.objects.create(
            name="Test Game",
            creator="Test Creator"
        )
        # Créer des médias non disponibles
        self.unavailable_book = Book.objects.create(
            title="Unavailable Book",
            author="Test Author",
            is_available=False
        )

    def test_available_media_view(self):
        """Test que la vue affiche correctement tous les médias disponibles"""
        response = self.client.get(reverse('available_media'))

        # Vérifier que la page charge correctement
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member/available_media.html')

        # Vérifier que les médias disponibles sont affichés
        self.assertContains(response, "Test Book")
        self.assertContains(response, "Test DVD")
        self.assertContains(response, "Test CD")
        self.assertContains(response, "Test Game")

        # Vérifier que les médias non disponibles ne sont pas affichés
        self.assertNotContains(response, "Unavailable Book")

        # Vérifier le contexte
        self.assertIn('books', response.context)
        self.assertIn('dvds', response.context)
        self.assertIn('cds', response.context)
        self.assertIn('boardgames', response.context)

        # Vérifier que seuls les médias disponibles sont dans le contexte
        self.assertEqual(len(response.context['books']), 1)
        self.assertTrue(all(book.is_available for book in response.context['books']))