from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from commons.serializers import SpecialtySerializer
from rest_framework.permissions import AllowAny
from tenants.models import Staff, Tenant, Booking, BookingDetailFile, BookingDetail
from tenants.serializers import DoctorSerializer, TenantSerializer, BookingSerializer, TenantStaffSpecialityDoctor, \
    BookingDetailFileSerializer


class TenantListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = Tenant.objects.all()
        serializer = TenantSerializer(tenant, many=True)
        return Response(serializer.data)


class TenantDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    # search_fields = ['last_name']
    # filter_backends = (filters.SearchFilter,)

    def get(self, request, pk):
        tenant = Tenant.objects.filter(subdomain_prefix=pk).first()
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)


class TenantStaffView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    def get(self, request, pk):
        staff_query = Staff.objects.filter(tenant__subdomain_prefix=pk).all()
        _staff = []
        for s in staff_query:
            staff = {
                'doctors': s.doctors,
                'specialty': s.specialty
            }
            doctor_serializer = TenantStaffSpecialityDoctor(staff)
            staff_data = doctor_serializer.data
            _staff.append(staff_data)
        return Response(_staff)


class TenantStaffSpecialitiesView(APIView):
    def get(self, request, pk):
        staff = Staff.objects.filter(tenant__subdomain_prefix=pk).all()
        specialties = []
        for s in staff:
            specialties.append(s.specialty)
        specialty_serializer = SpecialtySerializer(specialties, many=True)
        return Response(specialty_serializer.data)


class TenantStaffDoctorsBySpecialityView(APIView):
    def get(self, request, pk, specialty_id):
        query_staff = Staff.objects.filter(tenant__subdomain_prefix=pk) \
            .filter(specialty_id=specialty_id).all()

        doctors = []
        for s in query_staff:
            # query_doctor = s.doctors.all()
            query_doctor = s.doctors
            doctor_serializer = DoctorSerializer(query_doctor, many=True)
            docs = doctor_serializer.data
            for i in range(0, len(docs)):
                docs[i]['specialty'] = {
                    'id': s.specialty.id,
                    'name': s.specialty.name
                }
            doctors += docs
        return Response(doctors)


class TenantStaffDoctorsView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        doctors = []
        query_staff = Staff.objects.filter(tenant__subdomain_prefix=pk)
        for s in query_staff:
            if self.request.query_params.get("q") != None:
                filter_key = self.request.query_params.get("q")
                query_doctor = s.doctors.filter(profile__full_name__icontains=filter_key)
            else:
                query_doctor = s.doctors
            doctor_serializer = DoctorSerializer(query_doctor, many=True)
            docs = doctor_serializer.data
            for i in range(0, len(docs)):
                docs[i]['specialty'] = {
                    'id': s.specialty.id,
                    'name': s.specialty.name
                }
            doctors += docs
        return Response(doctors)


class TenantStaffDoctorDetailBySpecialityView(APIView):
    def get(self, request, pk, specialty_id, doctor_id):
        query_staff = Staff.objects.get(tenant__subdomain_prefix=pk, specialty_id=specialty_id)
        query_doctor = query_staff.doctors.get(profile__user=doctor_id)
        doctor_serializer = DoctorSerializer(query_doctor)
        doctor = doctor_serializer.data
        doctor['specialty'] = {
            'id': query_staff.specialty.id,
            'name': query_staff.specialty.name
        }
        return Response(doctor)


class TenantStaffDoctorBookingView(APIView):

    def post(self, request, pk):
        # doctor = User.objects.filter(id=pk).first()
        pass


class BookingView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None):
        if pk:
            try:
                booking = Booking.objects.get(bookingdetail__files=True, id=pk)
            except Booking.DoesNotExist:
                raise Http404()
            serializer = BookingSerializer(booking, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            booking = Booking.objects.select_related('bookingdetail').all()
            serializer = BookingSerializer(booking, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking_data = serializer.validated_data
        booking_detail_data = booking_data.pop('bookingdetail')
        booking = Booking.objects.create(**booking_data)
        BookingDetail.objects.create(booking_id=booking, **booking_detail_data)
        booking_serializer = BookingSerializer(booking)
        return Response(booking_serializer.data, status=status.HTTP_201_CREATED)

        # instance = serializer.save()
        # booking = BookingSerializer(instance)
        # return Response(booking.data, status=status.HTTP_201_CREATED)


from rest_framework.parsers import MultiPartParser, FormParser


class BookingFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)

    def get(self, request):
        booking = BookingDetailFile.objects.all()
        serializer = BookingDetailFileSerializer(booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        if 'file' not in request.FILES:
            return Response({'file error'}, status=status.HTTP_400_BAD_REQUEST)

        if 'booking_detail' not in request.data:
            return Response({'booking_detail error'}, status=status.HTTP_400_BAD_REQUEST)

        booking_detail = request.data.get('booking_detail')
        files = request.FILES.getlist('file')
        print('booking_detail', booking_detail)
        if len(files) > 1:  # Multiple Files
            for file in files:
                serializer_class = BookingDetailFileSerializer(data={'file': file, 'booking_detail': booking_detail})
                if serializer_class.is_valid():
                    serializer_class.save()
            print('finish for')
        else:  # Single File
            file = request.FILES['file']
            serializer_class = BookingDetailFileSerializer(data={'file': file, 'booking_detail': booking_detail})
            if serializer_class.is_valid():
                serializer_class.save()

        booking = BookingDetailFile.objects.filter(booking_detail=booking_detail)
        print(booking)
        serializer = BookingDetailFileSerializer(booking, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
