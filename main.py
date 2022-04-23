import os
import bojtomd

def main():
    while True:
        print('[ Input problem id. ]')
        print('[ Exit -> 0 ]')
        problem_id = int(input())

        if problem_id == 0:
            print('[ Bye ! ]')
            break

        status_code, data = bojtomd.fetch_solvedac(problem_id)
        if status_code == 200:
            print('[ Creating Markdown .. ]')
            path = bojtomd.write(data)
            print('[ Complte ! ]')
            print('[ %s ]\n' % path)
        else:
            print('[ Invalid problem id. ]')
            print('[ Please input valid problem id. ]')
            print('[ Exit -> 0 ]')

    os.system('pause')

if __name__ == "__main__":
    main()