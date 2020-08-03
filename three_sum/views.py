from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from three_sum.serializers import ThreeSumSerializer, TransactionSerializer
from three_sum.models import Transactions
import json
import datetime
# Create your views here.


class Solution:
    def __init__(self, input_list, target):
        self.input_list = input_list
        self.target = target

    def three_sum_solution(self):
        for num in self.input_list:
            self.target = self.target - num
            ans = self.__two_sum_solution()
            ans = [[num] + i for i in ans]
            return ans

    def __two_sum_solution(self): # Incapsulation
        nums = self.input_list
        seen_numbers = []
        ans = []
        for i in nums:
            remaining = self.target - i
            if remaining in seen_numbers:
                ans.append([remaining, i])
            else:
                seen_numbers.append(i)
        return ans


class ThreeSum(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_body = json.loads(request.body.decode('utf-8'))
        serializer = ThreeSumSerializer(data=request_body)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        input_list = request_body.get('input_list')
        target = request_body.get('sum')
        solution_object = Solution(input_list, target)
        answer = solution_object.three_sum_solution()
        if len(answer) > 0:
            self.record_transaction(input_list, target, answer, request.user)
            content = json.dumps(answer)
        else:
            content = 'No combination found'
        return Response(content, status=HTTP_200_OK)

    @staticmethod
    def record_transaction(input_list, target, answer, created_by):
        try:
            Transactions.objects.create(input_list=json.dumps(input_list),
                                        target=target,
                                        result=json.dumps(answer),
                                        user=created_by)
        except Exception as ex:
            with open('raw_data.txt', 'a+') as file:
                file.write(
                    "\nReceived At - {}, Input List - {}, Sum - {}, Result - {}, User - {}".format(datetime.datetime.now(),
                                                                                             input_list,
                                                                                             target,
                                                                                             answer,
                                                                                            created_by.id))
            file.close()
        return


class TransactionHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Transactions.objects.all().order_by('-queried_at')
        serializer = TransactionSerializer(qs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


