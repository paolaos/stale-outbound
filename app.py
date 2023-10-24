from bardapi import Bard

token = "cQhp2Rv0_ulDR1s7vHOx0zRavATQviMlw9AaruvlFgsZlTclotgNSXBAoHmnt49DELZHiA."
bard = Bard(token=token)
print(bard.get_answer("What is the meaning of life?")['content'])