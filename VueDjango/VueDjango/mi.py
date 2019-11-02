def get_pass():
        t={}
        with open('D:\\webcre\\Tryrtry\\VueDjango\\VueDjango\\mi.txt') as f:
                index = 0
                for i in f:
                        i = i.strip('\n')
                        t[index] = i
                        index+=1
                        
        return t
