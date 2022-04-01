import util

def main():
    print('[ Input problem id. ]')

    while True:
        problem_id = int(input())

        if problem_id == 0:
            print('[ Bye ! ]')
            break

        status_code, data = util.crawl(problem_id)
        if status_code == 200:
            print('[ Creating Markdown .. ]')
        else:
            print('[ Invalid problem id. ]')
            print('[ Please input valid problem id. ]')
            print('[ Exit -> 0 ]')

if __name__ == "__main__":
    main()