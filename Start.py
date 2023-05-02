base_rpm = 792
rpm_stat = 20
output = ""
talent = False
RPMCaps = [72, 88, 90, 99, 110, 120, 132, 165, 180, 198, 220, 264, 360, 396, 440, 495, 565, 660, 792, 990, 1320,
           1980, 3960]
nextrpm = None
output = ""
if base_rpm:
    try:
        base_rpm = float(base_rpm)
    except ValueError:
        base_rpm = ""
        base_rpm = False
else:
    base_rpm = False
if rpm_stat:
    try:
        stat = float(rpm_stat)
    except ValueError:
        rpm_stat = ""
        stat = False
else:
    stat = False
if talent:
    try:
        talent = float(talent)
    except ValueError:
        talent = ""
        talent = False
else:
    talent = False
if stat and stat >= 100 or talent and talent >= 100:
    output = "∞"
elif base_rpm and stat and talent:
    output = ((base_rpm / (1 - stat / 100)) / (1 - talent / 100))
elif base_rpm and stat:
    output = ((base_rpm / (1 - stat / 100)) / 1 - talent / 100)
elif base_rpm and talent:
    output = base_rpm / (1 - talent / 100)
elif base_rpm:
    output = base_rpm
else:
    output = 0
output = (f"{float(output):.2f}")
if output.replace('.', '', 1).isdigit():
    truerpm = float(output)
    if float(output) < 72:
        nextrpm = float(output) + 1
        actual = output
    else:
        for cap in RPMCaps:
            if not nextrpm:
                if float(output) >= cap:
                    actual = cap
                    pass
                else:
                    nextrpm = cap
    output += (f" | Actual: {actual}")
    print(output)