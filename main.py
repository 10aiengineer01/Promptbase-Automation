from ImagePromptAgency.agency import run_promptbase_agency

if __name__=="__main__":
    result = run_promptbase_agency(input("Should I create a image or a text prompt? :"))
    print(result)