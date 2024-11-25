from sqlmodel import Field, SQLModel


class StudentBase(SQLModel):
    name: str = Field()
    teacher: str = Field()
    age: int = Field()


class Student(StudentBase, table=True):
    id: int = Field(primary_key=True, default=None)
