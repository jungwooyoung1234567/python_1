# ------ GA Programming -----
# 00000 00000부터 11111 11111까지 가장 큰 이진 정수를 GA로 찾기
# 탐색 중에 해집단의 해들이 일정 비율 동일하게 수렴하면 최적 해로 수렴했다고 판단하고 탐색을 종료하도록 설계
# ---------------------------

# ----- 제약사항 ------
# pandas 모듈 사용 금지
# random 모듈만 사용, 필요시 numpy 사용 가능
# [chromosome, fitness]로 구성된 list 타입의 해 사용: ["1010", 10]
# population 형태는 다음과 같이 list 타입으로 규정: [["1010", 10], ["0001", 1], ["0011", 3]]
# --------------------

import random

# ----- 수정 가능한 파라미터 -----

params = {
    'MUT': 50,  # 변이확률(%)
    'END' : 0.9,  # 설정한 비율만큼 chromosome이 수렴하면 탐색을 멈추게 하는 파라미터 (%)
    'POP_SIZE' : 100,  # population size 10 ~ 100
    'RANGE' : 10,# chromosome의 표현 범위, 만약 10이라면 00000 00000 ~ 11111 11111까지임
    'NUM_OFFSPRING' : 10 # 한 세대에 발생하는 자식 chromosome의 수
    # 원하는 파라미터는 여기에 삽입할 것
    }
# ------------------------------

class GA():
    def __init__(self, parameters):
        self.params = {}
        for key, value in parameters.items():
            self.params[key] = value

    def get_fitness(self, chromosome):
        fitness =0
        chromo=chromosome[2:]
        fitness=int(chromo,2)
        # todo: 이진수 -> 십진수로 변환하여 fitness 구하기
        return fitness

    def print_average_fitness(self, population):
        # todo: population의 평균 fitness를 출력
        population_average_fitness = 0
        total=0
        for i in range(self.params["POP_SIZE"]):
            total=total+int(population[i][1])
        population_average_fitness=total/self.params["POP_SIZE"]    
        print(total)
        print("population 평균 fitness: {}".format(population_average_fitness))
        print("\n")   

    def sort_population(self, population):
        # todo: fitness를 기준으로 population을 내림차순 정렬하고 반환
        #버블정렬 로 오름차순 정렬을 실행합니다.
        for i in range(self.params["POP_SIZE"]):
          for j in range(self.params["POP_SIZE"]-1):
              if population[j][1]>population[j+1][1]:
                  population[j],population[j+1]=population[j+1],population[j]
        return population
    
    def sort_population_final(self, population):
        # todo: fitness를 기준으로 population을 내림차순 정렬하고 반환
        #버블정렬 로 내림차순 정렬을 실행합니다.
        for i in range(self.params["POP_SIZE"]):
          for j in range(self.params["POP_SIZE"]-1):
              if population[j][1]<population[j+1][1]:
                  population[j],population[j+1]=population[j+1],population[j]
        return population

    def selection_operater(self, population):
        # todo: 본인이 원하는 선택연산 구현(룰렛휠, 토너먼트, 순위 등), 선택압을 고려할 것, 한 쌍의 부모 chromosome 반환
        #토너먼트 선택 연산을 실행합니다.
        mom_ch = 0
        dad_ch = 0
        t=0.6
        k=3
        cnt=1
        rnd_list=[]
        ton_num=[]
        print("\n")
        # 2의k승만큼 부모 해인 population에서 랜덤으로 선택합니다.
        while len(rnd_list)<2**k:
            sel_num=random.choice(population)
            rnd_list.append(sel_num)
                 
        print("토너먼트 선택 연산을 위해 선택받은 값",rnd_list)
        print("\n")
        
        #이차원 리스트에서 정수 부분만 추출해서 새로운 리스트에 할당합니다.
        count=int(len(rnd_list))
        for i in range(0,2**k):
         ton_num.append(rnd_list[i][1])
         

        #랜덤 난수가 t보다 작을경우 작은수를 제거하는 토너먼트 연산 실행합니다.
        while(count>2):
           for i in range(0,int(count/2)):
               rnd_num=random.uniform(0,1)
               print("rnd_num",rnd_num)
               if t>rnd_num :
                   if ton_num[i]>=ton_num[i+1]:
                       ton_num.pop(i+1)
                   elif ton_num[i]<ton_num[i+1]:
                       ton_num.pop(i)
               elif t<rnd_num :
                   if ton_num[i]>=ton_num[i+1]:
                       ton_num.pop(i)
                   elif ton_num[i]<ton_num[i+1]:
                       ton_num.pop(i+1)
           count=count/2
           print(cnt,"번째 토너먼트 후 선택받은 값",ton_num)
           cnt=cnt+1
        mom_ch=ton_num[0]
        dad_ch=ton_num[1]
        print("토너먼트 후 선택받은 부모유전자",ton_num)
        print("\n")
        return mom_ch, dad_ch
       

    def crossover_operater(self, mom_cho, dad_cho):
        # todo: 본인이 원하는 교차연산 구현(point, pmx 등), 자식해 반환
        offs_list=[]
        total=0
        #교차 연산을 위해 리스트로 형변환을 실행합니다.
        mom_list=list(bin(mom_cho))[2:]
        dad_list=list(bin(dad_cho))[2:]
        #교차 연산을 위해 빈자리에 '0'을 추가합니다.
        while(len(mom_list)<=9) :
            mom_list.insert(0,'0')
        while(len(dad_list)<=9) :
             dad_list.insert(0,'0')
             
             
        print("10자리 변경후 유전자(모)",mom_list)
        print("10자리 변경후 유전자(부)",dad_list)   
        print("\n")
        
        mom_her=mom_list[0:5]
        dad_her=dad_list[5:10]
        #교차연산은 포인트 연산이용 1~5번째 순서는 모에게 6~10번째 순서는 부에서 물려받는 알고리즘 실행합니다.
        offs_list=mom_her+dad_her
        print("자식해 = ",offs_list)
        
        
        #리스트로 표시된 자식해를 이진수문자열로 바꾸는 과정 실행합니다.
        for i in range(0,10):
            if i ==9 and int(offs_list[9])==1:
                total=total+1
            else :
                total=total+(2**(9-i))*int(offs_list[i])
                
                
         
        offspring_cho = bin(total)[2:]
        print("2진수로 표시된 자식해:",offspring_cho)
        print("\n")
        
        return offs_list

    def mutation_operater(self, chromosome):        
        # todo: 변이가 결정되었다면 chromosome 안에서 랜덤하게 지정된 하나의 gene를 반대의 값(0->1, 1->0)으로 변이
        MUT=self.params['MUT']
        
        
        print("off_list",chromosome)
        
        rnd_num=random.randint(1,101)
        rnd_ary=random.randint(0,9)
        print("변이확률",rnd_num)
        print("바꿀자리:",rnd_ary+1)
        
        #MUT가 변이확률보다 높을 경우 랜덤한 위치에 변이를 실행합니다.
        if MUT > rnd_num :
            if chromosome[rnd_ary]=='0':
                print(rnd_ary+1,"번째의 값을 0=>1로 변환합니다.")
                chromosome[rnd_ary]='1'
            elif  chromosome[rnd_ary]=='1':
                print(rnd_ary+1,"번째의 값을 1=>0로 변환합니다.")
                chromosome[rnd_ary]='0'
                
        print("\n")        
        result_chromosome = chromosome
        
        print("변이연산이 끝난 유전자:",result_chromosome)
        print("\n") 
        return result_chromosome

    def replacement_operator(self, population, offsprings):
        # todo: 생성된 자식해들(offsprings)을 이용하여 기존 해집단(population)의 해를 대치하여 새로운 해집단을 return
        #자식 집단 해를 10진수로 변경후 리스트에 추가합니다.
        offs=[]
        for i in range(self.params['NUM_OFFSPRING']):
          total=0
          for j in range(0,10):
              if j==9 and int(offsprings[i][9])==1:
                  total+=1
              else:
                  total=total+(2**(9-j))*int(offsprings[i][j])
                
          offs.append(total)
          
          
        print("자식해집단:",offs)  
        print("부모해집단:",population)
        print("\n")   
       # population에서 10진수 만 추출후 리스트에 추가합니다.
        dec_par=[]
        for i in range(self.params["POP_SIZE"]):
            dec_par.append(population[i][1])
        print("10진수만 추출한 부모집단의 해집단",dec_par)
        
        
        print("\n")   
        #부모해집단 중 제일 작은 값을 제거 후 자식 해를 부모해집단에 추가하는 대체연산을 실행합니다.
        for i in range(self.params["NUM_OFFSPRING"]):
           print("가장작은해의 index번호",dec_par.index(min(dec_par))+1)
           population.pop(dec_par.index(min(dec_par)))
           dec_par.pop(dec_par.index(min(dec_par)))
           population.append([bin(offs[i])[2:],offs[i]])
           dec_par.append(offs[i])
        print("대치연산이 완료된 해집단:",population) 
            
        return population   
            
        
    # 해 탐색(GA) 함수
    def search(self):
        generation = 0  # 현재 세대 수
        population = [] # 해집단
        offsprings = [] # 자식해집단  
        off_switch=0

        # 1. 초기화: 랜덤하게 해를 초기화
        for i in range(self.params["POP_SIZE"]):
             # todo: random 모듈을 사용하여 랜덤한 해 생성, self.params["range"]를 사용할 것
             # todo: fitness를 구하는 함수인 self.get_fitness()를 만들어서 fitness를 구할 것
             # todo: 정렬함수인 self.sort_population()을 사용하여 population을 정렬할 것 
             chr_bin=bin(random.getrandbits(self.params["RANGE"]))
             population.append([chr_bin[2:],self.get_fitness(chr_bin)]) 
            
            
        population=self.sort_population(population)
        print("initialzed population : \n", population, "\n\n")
       
           

        while 1:
            for i in range(self.params["NUM_OFFSPRING"]):
       
                # 2. 선택 연산
                mom_ch, dad_ch = self.selection_operater(population)

                # 3. 교차 연산
                offspring = self.crossover_operater(mom_ch, dad_ch)

                # 4. 변이 연산
                # todo: 변이 연산여부를 결정, self.params["MUT"]에 따라 변이가 결정되지 않으면 변이연산 수행하지 않음
                offspring = self.mutation_operater(offspring)

                offsprings.append(offspring)
            for i in range(len(offsprings)) :
             print("offsprings",i+1,offsprings[i])
            print("\n")  
                

            # 5. 대치 연산
            population = self.replacement_operator(population, offsprings)

            self.print_average_fitness(population) # population의 평균 fitness를 출력함으로써 수렴하는 모습을 보기 위한 기능
  
            # 6. 알고리즘 종료 조건 판단
            # todo population이 전체 중 self.params["END"]의 비율만큼 동일한 해를 갖는다면 수렴했다고 판단하고 탐색 종료
            dec_number=[]
           
            for i in range(self.params["POP_SIZE"]) :
                dec_number.append(population[i][1])
        
            for i in range(self.params["POP_SIZE"]) :
                if dec_number.count(dec_number[i]) >= int(self.params["POP_SIZE"]*self.params["END"]):
                     off_switch=1
                     print("동일한 해의 갯수:",dec_number.count(dec_number[i]))
                     break
                   
                 
            generation+=1
            print("generation",generation)
            if off_switch==1 :
                print(self.sort_population_final(population))
                break
            offsprings=[]
        # 최종적으로 얼마나 소요되었는지의 세대수, 수렴된 chromosome과 fitness를 출력
        print("탐색이 완료되었습니다. \t 최종 세대수: {},\t 최종 해: {},\t 최종 적합도: {}".format(generation, population[0][0], population[0][1]))


if __name__ == "__main__":
    ga = GA(params)
    ga.search()



