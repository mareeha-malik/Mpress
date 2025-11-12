from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from .models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError


class ProfileModelTests(TestCase):

    def test_profile_created_on_user_creation(self):
        u = User.objects.create_user(username='alice', password='pass')
        # Profile should be auto-created by signals
        self.assertTrue(hasattr(u, 'profile'))
        self.assertIsInstance(u.profile, Profile)
        self.assertEqual(str(u.profile), f"Profile of {u.username}")


class ProfileFormValidationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pass')

    def test_avatar_accepts_image(self):
        # small dummy PNG file header bytes
        small_png = SimpleUploadedFile('test.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')
        profile = self.user.profile
        profile.avatar = small_png
        profile.save()
        self.assertTrue(profile.avatar.name.endswith('test.png'))

    def test_avatar_rejects_non_image(self):
        bad_file = SimpleUploadedFile('test.txt', b'not-an-image', content_type='text/plain')
        form_data = {'bio': 'hello'}
        form_files = {'avatar': bad_file}
        from .forms import ProfileForm
        form = ProfileForm(data=form_data, files=form_files, instance=self.user.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('avatar', form.errors)

    def test_avatar_rejects_large_file(self):
        # create a large fake image (>3MB)
        large_content = b'a' * (3 * 1024 * 1024)
        large_img = SimpleUploadedFile('big.png', large_content, content_type='image/png')
        form_data = {'bio': 'big'}
        form_files = {'avatar': large_img}
        from .forms import ProfileForm
        form = ProfileForm(data=form_data, files=form_files, instance=self.user.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('avatar', form.errors)
