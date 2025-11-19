time_scale = 0.5
time_1 = int(400*time_scale)
time_3 = int(1600*time_scale)
time_4 = int(2000*time_scale)
action_groups_ato6 = [
      [#1[置中]
          {'id': 1, 'position': 300, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 300, 'time': time_3},
          {'id': 4, 'position': 900, 'time': time_3},
          {'id': 5, 'position': 700, 'time': time_3},
          {'id': 6, 'position': 500, 'time': time_3}
      ],
      [#2[a上張1]
          {'id': 1, 'position': 300, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 150, 'time': time_3},
          {'id': 4, 'position': 800, 'time': time_3},
          {'id': 5, 'position': 500, 'time': time_3},
          {'id': 6, 'position': 790, 'time': time_3}
      ],
      [#3[a上張2]
          {'id': 1, 'position': 200, 'time': time_1},
          {'id': 2, 'position': 500, 'time': time_1},
          {'id': 3, 'position': 150, 'time': time_1},
          {'id': 4, 'position': 800, 'time': time_1},
          {'id': 5, 'position': 450, 'time': time_1},
          {'id': 6, 'position': 790, 'time': time_1}
      ],
      [#4[a上張3]
          {'id': 1, 'position': 200, 'time': time_3},
          {'id': 2, 'position': 430, 'time': time_3},
          {'id': 3, 'position': 150, 'time': time_3},
          {'id': 4, 'position': 800, 'time': time_3},
          {'id': 5, 'position': 450, 'time': time_3},
          {'id': 6, 'position': 800, 'time': time_3}
      ],
      [#5[a上抓1]
          {'id': 1, 'position': 600, 'time': time_4},
          {'id': 2, 'position': 430, 'time': time_4},
          {'id': 3, 'position': 150, 'time': time_4},
          {'id': 4, 'position': 800, 'time': time_4},
          {'id': 5, 'position': 465, 'time': time_4},
          {'id': 6, 'position': 800, 'time': time_4}
      ],
      [#6[6上抓1]
          {'id': 1, 'position': 600, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 180, 'time': time_3},
          {'id': 4, 'position': 750, 'time': time_3},
          {'id': 5, 'position': 430, 'time': time_3},
          {'id': 6, 'position': 300, 'time': time_3}
      ],
      [#7[6上抓2]
          {'id': 1, 'position': 600, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 180, 'time': time_3},
          {'id': 4, 'position': 750, 'time': time_3},
          {'id': 5, 'position': 415, 'time': time_3},
          {'id': 6, 'position': 300, 'time': time_3}
      ],
      [#8[6上放1]
          {'id': 1, 'position': 300, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 200, 'time': time_3},
          {'id': 4, 'position': 750, 'time': time_3},
          {'id': 5, 'position': 400, 'time': time_3},
          {'id': 6, 'position': 300, 'time': time_3}
      ],
      [#9[6上放2]
          {'id': 1, 'position': 300, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 200, 'time': time_3},
          {'id': 4, 'position': 750, 'time': time_3},
          {'id': 5, 'position': 430, 'time': time_3},
          {'id': 6, 'position': 300, 'time': time_3}
      ],
      [#10[置中]
          {'id': 1, 'position': 300, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 300, 'time': time_3},
          {'id': 4, 'position': 900, 'time': time_3},
          {'id': 5, 'position': 700, 'time': time_3},
          {'id': 6, 'position': 500, 'time': time_3}
      ]
  ]
# 反轉動作組順序，從1點移動回a點
action_groups_6toa = list(reversed(action_groups_ato6))
























