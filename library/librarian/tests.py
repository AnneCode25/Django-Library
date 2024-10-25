from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from shared_models.models import Member, Book, DVD, CD, Loan, BoardGame
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.auth import get_user_model


class MemberModelTest(TestCase):
    def setUp(self):
        # Création d'un membre pour les tests
        self.member = Member.objects.create(
            first_name="Jean",
            last_name="Test"
        )

        # Création de quelques médias pour les tests
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

    def test_member_creation(self):
        self.assertEqual(self.member.first_name, "Jean")
        self.assertEqual(self.member.last_name, "Test")
        self.assertEqual(str(self.member), "Test, Jean")

    def test_can_borrow_limit(self):
        # Test limite de 3 emprunts
        self.assertTrue(self.member.can_borrow())

        # Créer 3 emprunts
        for i in range(3):
            content_type = ContentType.objects.get_for_model(Book)
            Loan.objects.create(
                member=self.member,
                content_type=content_type,
                object_id=self.book.id
            )

        # Vérifier qu'un 4ème emprunt est impossible
        self.assertFalse(self.member.can_borrow())

    def test_has_overdue_loans(self):
        # Créer un emprunt en retard
        content_type = ContentType.objects.get_for_model(Book)
        Loan.objects.create(
            member=self.member,
            content_type=content_type,
            object_id=self.book.id,
            loan_date=timezone.now() - timedelta(days=8)  # 8 jours = en retard
        )

        self.assertTrue(self.member.has_overdue_loans())


class MediaModelTest(TestCase):
    def setUp(self):
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

    def test_media_creation(self):
        self.assertEqual(str(self.book), "Test Book")
        self.assertEqual(str(self.dvd), "Test DVD")
        self.assertEqual(str(self.cd), "Test CD")
        self.assertTrue(self.book.is_available)

    def test_media_availability(self):
        member = Member.objects.create(first_name="Test", last_name="User")
        content_type = ContentType.objects.get_for_model(Book)

        # Créer un emprunt
        Loan.objects.create(
            member=member,
            content_type=content_type,
            object_id=self.book.id
        )

        self.book.is_available = False
        self.book.save()

        self.assertFalse(self.book.is_available)


# Dans librarian/tests.py

class BoardGameModelTest(TestCase):
    def setUp(self):
        self.boardgame = BoardGame.objects.create(
            name="Monopoly",
            creator="Charles Darrow"
        )

    def test_boardgame_creation(self):
        """Test la création d'un jeu de plateau"""
        self.assertEqual(self.boardgame.name, "Monopoly")
        self.assertEqual(self.boardgame.creator, "Charles Darrow")
        self.assertEqual(str(self.boardgame), "Monopoly")


class BoardGameViewsTest(TestCase):
    def setUp(self):
        # Créer un utilisateur bibliothécaire pour les tests
        User = get_user_model()
        self.librarian = User.objects.create_user(
            username='testlibrarian',
            password='testpass123',
            is_librarian=True
        )
        # Connexion du bibliothécaire
        self.client.login(username='testlibrarian', password='testpass123')

        # Créer un jeu de test
        self.boardgame = BoardGame.objects.create(
            name="Monopoly",
            creator="Charles Darrow"
        )

    def test_boardgame_list_view(self):
        """Test l'affichage de la liste des jeux"""
        response = self.client.get(reverse('boardgame_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/boardgame_list.html')
        self.assertContains(response, "Monopoly")
        self.assertContains(response, "Charles Darrow")

    def test_boardgame_add_view(self):
        """Test l'ajout d'un nouveau jeu"""
        # Test GET
        response = self.client.get(reverse('boardgame_add'))
        self.assertEqual(response.status_code, 200)

        # Test POST avec données valides
        data = {
            'name': 'Risk',
            'creator': 'Albert Lamorisse'
        }
        response = self.client.post(reverse('boardgame_add'), data)
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertTrue(BoardGame.objects.filter(name='Risk').exists())

    def test_boardgame_detail_view(self):
        """Test la vue détaillée d'un jeu"""
        # Test GET
        response = self.client.get(reverse('boardgame_detail', args=[self.boardgame.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Monopoly")

        # Test modification
        data = {
            'name': 'Monopoly Edition Spéciale',
            'creator': 'Charles Darrow',
            'update': 'update'
        }
        response = self.client.post(reverse('boardgame_detail', args=[self.boardgame.id]), data)
        self.boardgame.refresh_from_db()
        self.assertEqual(self.boardgame.name, 'Monopoly Edition Spéciale')

        # Test suppression
        response = self.client.post(
            reverse('boardgame_detail', args=[self.boardgame.id]),
            {'delete': 'delete'}
        )
        self.assertFalse(BoardGame.objects.filter(id=self.boardgame.id).exists())

    def test_unauthorized_access(self):
        """Test l'accès non autorisé"""
        # Déconnexion
        self.client.logout()

        # Test accès aux vues protégées
        urls = [
            reverse('boardgame_list'),
            reverse('boardgame_add'),
            reverse('boardgame_detail', args=[self.boardgame.id])
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirection vers login


class LoanModelTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            first_name="Jean",
            last_name="Test"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            is_available=True
        )

    def test_loan_creation(self):
        content_type = ContentType.objects.get_for_model(Book)
        loan = Loan.objects.create(
            member=self.member,
            content_type=content_type,
            object_id=self.book.id
        )

        self.assertEqual(loan.member, self.member)
        self.assertEqual(loan.item, self.book)
        self.assertIsNone(loan.return_date)

    def test_loan_is_overdue(self):
        content_type = ContentType.objects.get_for_model(Book)
        loan = Loan.objects.create(
            member=self.member,
            content_type=content_type,
            object_id=self.book.id,
            loan_date=timezone.now() - timedelta(days=8)
        )

        self.assertTrue(loan.is_overdue())

    def test_loan_due_date(self):
        content_type = ContentType.objects.get_for_model(Book)
        loan = Loan.objects.create(
            member=self.member,
            content_type=content_type,
            object_id=self.book.id
        )

        expected_due_date = loan.loan_date + timedelta(days=7)
        self.assertEqual(loan.due_date(), expected_due_date)





class LibrarianViewsTest(TestCase):
    def setUp(self):
        # Créer un utilisateur bibliothécaire pour les tests
        User = get_user_model()
        self.librarian = User.objects.create_user(
            username='testlibrarian',
            password='testpass123',
            is_librarian=True
        )

        # Créer un client pour les tests
        self.client = Client()

        # Connexion du bibliothécaire
        self.client.login(username='testlibrarian', password='testpass123')

        # Créer des objets de test
        self.member = Member.objects.create(
            first_name="Test",
            last_name="User"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            is_available=True
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/dashboard.html')

    def test_member_list_view(self):
        response = self.client.get(reverse('member_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'librarian/member_list.html')
        self.assertIn('members', response.context)

    def test_add_member_view(self):
        # Test GET request
        response = self.client.get(reverse('add_member'))
        self.assertEqual(response.status_code, 200)

        # Test POST request
        data = {
            'first_name': 'New',
            'last_name': 'Member'
        }
        response = self.client.post(reverse('add_member'), data)
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertTrue(Member.objects.filter(first_name='New', last_name='Member').exists())

    def test_member_detail_view(self):
        # Test GET request
        response = self.client.get(reverse('member_detail', args=[self.member.id]))
        self.assertEqual(response.status_code, 200)

        # Test UPDATE
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'update': 'update'
        }
        response = self.client.post(reverse('member_detail', args=[self.member.id]), data)
        self.member.refresh_from_db()
        self.assertEqual(self.member.first_name, 'Updated')

        # Test DELETE
        response = self.client.post(reverse('member_detail', args=[self.member.id]), {'delete': 'delete'})
        self.assertFalse(Member.objects.filter(id=self.member.id).exists())

    def test_borrow_item_view(self):
        response = self.client.get(reverse('borrow_item'))
        self.assertEqual(response.status_code, 200)

        # Test emprunt
        data = {
            'member': self.member.id,
            'item_type': 'book',
            'item': self.book.id
        }
        response = self.client.post(reverse('borrow_item'), data)
        self.assertTrue(Loan.objects.filter(member=self.member, object_id=self.book.id).exists())

    def test_return_item_view(self):
        # Créer un emprunt
        content_type = ContentType.objects.get_for_model(Book)
        loan = Loan.objects.create(
            member=self.member,
            content_type=content_type,
            object_id=self.book.id
        )

        # Test page de retour
        response = self.client.get(reverse('return_item'))
        self.assertEqual(response.status_code, 200)

        # Test confirmation de retour
        response = self.client.post(reverse('confirm_return', args=[loan.id]))
        loan.refresh_from_db()
        self.assertIsNotNone(loan.return_date)

    def test_media_list_view(self):
        response = self.client.get(reverse('media_list', args=['book']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)

    def test_unauthorized_access(self):
        # Déconnexion
        self.client.logout()

        # Test accès non autorisé
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login