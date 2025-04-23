import grpc

import course_service_pb2
import course_service_pb2_grpc


def run():
    # Устанавливаем соединение с сервером
    channel = grpc.insecure_channel('localhost:50051')
    stub = course_service_pb2_grpc.CourseServiceStub(channel)

    # Отправляем запрос с ID курса
    request = course_service_pb2.GetCourseRequest(course_id="233196")
    response = stub.GetCourse(request)
    print(response)


if __name__ == "__main__":
    run()