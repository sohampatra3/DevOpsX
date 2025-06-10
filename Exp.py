import redis

r = redis.Redis(host='redis', port=6379)
r.set('key', 'Hello from Docker Compose!')
print(r.get('key').decode())


print("soham")
name="soham"
age=22
height=5.11
is_student=False
print(name,age,height,is_student)
soham=int(input("enter your name"))
my_heighr=float(input("put your height"))

