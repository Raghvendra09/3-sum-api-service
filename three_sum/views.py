from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from three_sum.serializers import ThreeSumSerializer, TransactionSerializer
from three_sum.models import Transactions
import json
import datetime


class Solution:
    def __init__(self, input_list, target):
        self.input_list = sorted(input_list)
        self.target = target
        self.ans = []

    def three_sum_solution(self):
        for position in range(len(self.input_list)):
            if (position == 0 or self.input_list[position] != self.input_list[position-1]) and self.input_list[position] <= 0:
                self.__two_sum_solution(position)
        return self.ans

    def __two_sum_solution(self, position):

        target = self.target - self.input_list[position]
        low, high = position+1, len(self.input_list) - 1
        while low < high:
            sum = self.input_list[low] + self.input_list[high]
            if sum < target or (low > (position + 1) and self.input_list[low] == self.input_list[low-1]):
                low += 1
            elif sum > target or (high < len(self.input_list) - 1 and self.input_list[high] == self.input_list[high+1]):
                high -= 1
            else:
                self.ans.append([self.input_list[position], self.input_list[low], self.input_list[high]])
                low += 1
                high -= 1
        return


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


