from rest_framework import serializers
from meeting.serializers import MeetingSerializer
from negotiation.serializers import NegotiationSerializer
from qualified.serializers import QualifiedSerializer
from won.serializers import WonSerializer
from accounts.models import Account, Tags
from common.models import Profile
from common.serializer import (
    AttachmentsSerializer,
    LeadCommentSerializer,
    OrganizationSerializer,
    ProfileSerializer,
    UserSerializer,
)
from contacts.serializer import ContactSerializer
from leads.models import Company, Lead
from teams.serializer import TeamsSerializer


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name", "slug")


class CompanySwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("name",)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "org")


class LeadSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)
    assigned_to = ProfileSerializer(read_only=True, many=True)
    created_by = UserSerializer()
    country = serializers.SerializerMethodField()
    tags = TagsSerializer(read_only=True, many=True)
    lead_attachment = AttachmentsSerializer(read_only=True, many=True)
    teams = TeamsSerializer(read_only=True, many=True)
    lead_comments = LeadCommentSerializer(read_only=True, many=True)
    meetings = MeetingSerializer(many=True, read_only=True)
    opportunity = OrganizationSerializer(read_only=True)
    qualified = QualifiedSerializer(read_only=True)
    negotiation = NegotiationSerializer(read_only=True)
    won = WonSerializer(read_only=True)

    def get_country(self, obj):
        return obj.get_country_display()

    class Meta:
        model = Lead
        # fields = ‘__all__’
        fields = (
            "id",
            "title",
            "first_name",
            "last_name",
            "phone",
            "email",
            "status",
            "source",
            "address_line",
            "contacts",
            "street",
            "city",
            "state",
            "postcode",
            "country",
            "website",
            "description",
            "lead_attachment",
            "lead_comments",
            "assigned_to",
            "account_name",
            "opportunity_amount",
            "created_by",
            "created_at",
            "is_active",
            "enquiry_type",
            "tags",
            "created_from_site",
            "teams",
            "skype_ID",
            "industry",
            "company",
            "organization",
            "probability",
            "close_date",
            "meetings",
            "opportunity",
            "qualified",
            "negotiation",
            "won",
        )

    def create(self, validated_data):
        assigned_to_data = validated_data.pop('assigned_to', [])
        lead = Lead.objects.create(**validated_data)

        # Increase workload for newly assigned profiles
        for profile_data in assigned_to_data:
            profile = Profile.objects.get(id=profile_data['id'])
            profile.workload += 1
            profile.save()
            lead.assigned_to.add(profile)

        lead.save()
        return lead

    def update(self, instance, validated_data):
        assigned_to_data = validated_data.pop('assigned_to', [])
        current_assigned_profiles = set(instance.assigned_to.all())
        new_assigned_profiles = set()

        # Increase workload for newly assigned profiles
        for profile_data in assigned_to_data:
            profile = Profile.objects.get(id=profile_data['id'])
            if profile not in current_assigned_profiles:
                profile.workload += 1
                profile.save()
            new_assigned_profiles.add(profile)
            instance.assigned_to.add(profile)

        # Decrease workload for profiles that are no longer assigned
        for profile in current_assigned_profiles:
            if profile not in new_assigned_profiles:
                profile.workload -= 1
                profile.save()
                instance.assigned_to.remove(profile)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class LeadCreateSerializer(serializers.ModelSerializer):
    probability = serializers.IntegerField(max_value=100)

    def __init__(self, *args, **kwargs):
        request_obj = kwargs.pop("request_obj", None)
        super().__init__(*args, **kwargs)
        if self.initial_data and self.initial_data.get("status") == "converted":
            self.fields["account_name"].required = True
            self.fields["email"].required = True
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False
        self.fields["title"].required = True
        self.org = request_obj.profile.org

        if self.instance:
            if self.instance.created_from_site:
                prev_choices = self.fields["source"]._get_choices()
                prev_choices = prev_choices + [("micropyramid", "Micropyramid")]
                self.fields["source"]._set_choices(prev_choices)

    def validate_account_name(self, account_name):
        if self.instance:
            if (
                Account.objects.filter(name__iexact=account_name, org=self.org)
                .exclude(id=self.instance.id)
                .exists()
            ):
                raise serializers.ValidationError(
                    "Account already exists with this name"
                )
        else:
            if Account.objects.filter(name__iexact=account_name, org=self.org).exists():
                raise serializers.ValidationError(
                    "Account already exists with this name"
                )
        return account_name

    def validate_title(self, title):
        if self.instance:
            if (
                Lead.objects.filter(title__iexact=title, org=self.org)
                .exclude(id=self.instance.id)
                .exists()
            ):
                raise serializers.ValidationError("Lead already exists with this title")
        else:
            if Lead.objects.filter(title__iexact=title, org=self.org).exists():
                raise serializers.ValidationError("Lead already exists with this title")
        return title

    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "account_name",
            "title",
            "phone",
            "email",
            "status",
            "source",
            "website",
            "description",
            "address_line",
            # "contacts",
            "street",
            "city",
            "state",
            "postcode",
            "opportunity_amount",
            "country",
            "org",
            "skype_ID",
            "industry",
            "company",
            "organization",
            "probability",
            "close_date",
            # "lead_attachment",
        )

class LeadCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["title","first_name","last_name","account_name","phone","email","lead_attachment","opportunity_amount","website",
                "description","teams","assigned_to","contacts","status","source","address_line","street","city","state","postcode",
                "country","tags","company","probability","industry","skype_ID"]


class CreateLeadFromSiteSwaggerSerializer(serializers.Serializer):
    apikey=serializers.CharField()
    title=serializers.CharField()
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    phone=serializers.CharField()
    email=serializers.CharField()
    source=serializers.CharField()
    description=serializers.CharField()


class LeadDetailEditSwaggerSerializer(serializers.Serializer):
    comment = serializers.CharField()
    lead_attachment = serializers.FileField()

class LeadCommentEditSwaggerSerializer(serializers.Serializer):
    comment = serializers.CharField()

class LeadUploadSwaggerSerializer(serializers.Serializer):
    leads_file = serializers.FileField()

