from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.parsers import JSONParser
from chat.models import FriendRequest, Contact, Room, Profile
import json
import channels


class FriendRequestModelTest(TestCase):
    def create_and_accept_friend_request(self):
        test_user_1 = User.objects.create(username="test_user_1", password="test_user_1_password")
        test_user_2 = User.objects.create(username="test_user_2", password="test_user_2_password")

        friend_request = FriendRequest(user=test_user_1, other=test_user_2, accepted=True)
        friend_request.save()

        return test_user_1, test_user_2, friend_request
    
    def test_contact_created_when_friend_request_accepted(self):
        test_user_1, test_user_2, friend_request = self.create_and_accept_friend_request()

        self.assertEqual(test_user_1.contacts.filter(other=test_user_2).count(), 1)
        self.assertEqual(test_user_2.contacts.filter(other=test_user_1).count(), 1)

    def test_room_created_when_friend_request_accepted(self):
        test_user_1, test_user_2, friend_request = self.create_and_accept_friend_request()

        if test_user_1.id < test_user_2.id:
            room_name=f"room-{test_user_1.id}-{test_user_2.id}"
        else:
            room_name=f"room-{test_user_2.id}-{test_user_1.id}"

        self.assertEqual(Room.objects.filter(name=room_name).count(), 1)

    def test_second_contact_not_created_when_friend_request_accepted_and_saved_for_a_second_time(self):
        test_user_1, test_user_2, friend_request = self.create_and_accept_friend_request()
        friend_request.save()

        self.assertEqual(Contact.objects.filter(user=test_user_1, other=test_user_2).count(), 1)
        self.assertEqual(Contact.objects.filter(user=test_user_2, other=test_user_1).count(), 1)

    def test_second_room_not_created_when_friend_request_accepted_and_saved_for_a_second_time(self):
        test_user_1, test_user_2, friend_request = self.create_and_accept_friend_request()
        friend_request.save()

        if test_user_1.id < test_user_2.id:
            room_name=f"room-{test_user_1.id}-{test_user_2.id}"
        else:
            room_name=f"room-{test_user_2.id}-{test_user_1.id}"

        self.assertEqual(Room.objects.filter(name=room_name).count(), 1)


class ProfileModelTest(TestCase):
    def create_user(self):
        test_user = User.objects.create(username="test_user", password="test_user_password")
        return test_user

    def test_profile_created_when_user_created(self):
        test_user = self.create_user()

        self.assertEqual(Profile.objects.filter(user=test_user).count(), 1)

    def test_user_is_online_if_user_made_a_request_recently(self):
        test_user = self.create_user()
        self.client.force_login(test_user)
        self.client.get(reverse('index'))

        self.assertEqual(test_user.profile.online(), True)


class FriendRequestViewTest(TestCase):
    def create_two_test_users(self):
        test_user_1 = User.objects.create(username="test_user_1", password="test_user_1_password")
        test_user_2 = User.objects.create(username="test_user_2", password="test_user_2_password")
        return test_user_1, test_user_2

    def test_friend_request_is_created(self):
        test_user_1, test_user_2 = self.create_two_test_users()
        self.client.force_login(test_user_1)
        response = self.client.post(reverse('friend_request'), {
            'username': test_user_2.username, 'user': test_user_1.id
        })

        self.assertEqual(FriendRequest.objects.filter(user=test_user_1, other=test_user_2).count(), 1)


class ContactsViewTest(TestCase):
    def create_three_test_users(self):
        test_user_1 = User.objects.create(username="test_user_1", password="test_user_1_password")
        test_user_2 = User.objects.create(username="test_user_2", password="test_user_2_password")
        test_user_3 = User.objects.create(username="test_user_3", password="test_user_3_password")
        return test_user_1, test_user_2, test_user_3

    def test_all_filter(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()
        
        FriendRequest.objects.create(user=test_user_1, other=test_user_2, accepted=True)
        FriendRequest.objects.create(user=test_user_1, other=test_user_3, accepted=True)

        self.client.force_login(test_user_1)
        
        response = self.client.get(reverse('contacts')+'?filter=all')
        data = json.loads(response.json())

        self.assertEqual(len(data), 2)

    def test_online_filter(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()
        
        FriendRequest.objects.create(user=test_user_1, other=test_user_2, accepted=True)
        FriendRequest.objects.create(user=test_user_1, other=test_user_3, accepted=True)

        self.client.force_login(test_user_2)
        self.client.get(reverse('index'))

        self.client.force_login(test_user_1)

        response = self.client.get(reverse('contacts')+'?filter=online')
        data = json.loads(response.json())

        self.assertEqual(len(data), 1)

    def test_offline_filter_2(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()
        
        FriendRequest.objects.create(user=test_user_1, other=test_user_2, accepted=True)
        FriendRequest.objects.create(user=test_user_1, other=test_user_3, accepted=True)

        self.client.force_login(test_user_1)

        response = self.client.get(reverse('contacts')+'?filter=offline')
        data = json.loads(response.json())

        self.assertEqual(len(data), 2)

    def test_offline_filter_2(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()
        
        FriendRequest.objects.create(user=test_user_1, other=test_user_2, accepted=True)
        FriendRequest.objects.create(user=test_user_1, other=test_user_3, accepted=True)

        self.client.force_login(test_user_2)
        self.client.get(reverse('index'))

        self.client.force_login(test_user_1)

        response = self.client.get(reverse('contacts')+'?filter=offline')
        data = json.loads(response.json())

        self.assertEqual(len(data), 1)


class SearchViewTest(TestCase):
    def create_three_test_users(self):
        test_user_1 = User.objects.create(username="test_user_1", password="test_user_1_password")
        test_user_2 = User.objects.create(username="test_user_2", password="test_user_2_password")
        test_user_3 = User.objects.create(username="test_user_3", password="test_user_3_password")
        return test_user_1, test_user_2, test_user_3

    def test_1(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()
        
        FriendRequest.objects.create(user=test_user_1, other=test_user_2, accepted=True)
        FriendRequest.objects.create(user=test_user_1, other=test_user_3, accepted=True)

        self.client.force_login(test_user_1)
        
        response = self.client.get(reverse('search', args=('t',)))
        data = json.loads(response.json())

        self.assertEqual(len(data), 2)

    def test_2(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()
        
        FriendRequest.objects.create(user=test_user_1, other=test_user_2, accepted=True)
        FriendRequest.objects.create(user=test_user_1, other=test_user_3, accepted=True)

        self.client.force_login(test_user_1)
        
        response = self.client.get(reverse('search', args=('test_user_3',)))
        data = json.loads(response.json())

        self.assertEqual(len(data), 1)


class NotificationsViewTest(TestCase):
    def create_three_test_users(self):
        test_user_1 = User.objects.create(username="test_user_1", password="test_user_1_password")
        test_user_2 = User.objects.create(username="test_user_2", password="test_user_2_password")
        test_user_3 = User.objects.create(username="test_user_3", password="test_user_3_password")
        return test_user_1, test_user_2, test_user_3

    def test_all_filter(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()

        FriendRequest.objects.create(user=test_user_2, other=test_user_1, accepted=False)
        FriendRequest.objects.create(user=test_user_3, other=test_user_1, accepted=True)
        
        self.client.force_login(test_user_1)

        response = self.client.get(reverse('notifications')+"?filter=all")
        data = json.loads(response.json())

        self.assertEqual(len(data), 1)

    def test_accept_friend_request(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()

        friend_request = FriendRequest.objects.create(user=test_user_2, other=test_user_1, accepted=False)
        
        self.client.force_login(test_user_1)

        response = self.client.post(reverse('accept_friend_request', args=(friend_request.id,)))

        self.assertEqual(FriendRequest.objects.get(id=friend_request.id).accepted, True)

    def test_reject_friend_request(self):
        test_user_1, test_user_2, test_user_3 = self.create_three_test_users()

        friend_request = FriendRequest.objects.create(user=test_user_2, other=test_user_1, accepted=False)
        
        self.client.force_login(test_user_1)

        response = self.client.post(reverse('reject_friend_request', args=(friend_request.id,)))

        self.assertEqual(FriendRequest.objects.filter(user=test_user_2, other=test_user_1).count(), 0)