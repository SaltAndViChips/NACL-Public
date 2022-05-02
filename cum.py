def main():
    levelxp = 0
    totalxp = 0

    try:
        costperxp = float(input("How Much IC do you want to charge per level?"))
        total_levels = int(input("How many levels do you want done?"))
        for level in range(total_levels):
            levelxp += 100
            totalxp += levelxp
            print (f"{level+1}: {levelxp}  | Total: {totalxp} | Cost = {totalxp*costperxp}")
    except(ValueError):
        print()
        main()
main()