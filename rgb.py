def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + int(hlen / 3)], 16) for i in range(0, hlen, int(hlen / 3)))


judge_color = ['#c3c45b', '#c3c45b', '#c3c45b', '#cf2904', '#098ae0', '#f48a1c', '#8a30c9', '#837b8a']

for c in judge_color:
    print(f"{c}: {hex_to_rgb(c)}")
