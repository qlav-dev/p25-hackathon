import pandas as pd



class humain:

    def __init__(self, prenom: str):
        self.prenom = prenom

    def __len__(self):
        return len(self.prenom)

    def __getitem__(self, i):
        return self.prenom[i]

class humain2(humain):
    def __init__(self, prenom, age):
        super().__init__(prenom)
        self.age = age
    
    def __repr__(self):
        return f"Bonjour, je suis {self.prenom}, j'ai {self.age} ans"

x = humain("aaa")


