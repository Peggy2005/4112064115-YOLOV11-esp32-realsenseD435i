time_scale = 0.8
time_1 = int(400*time_scale)
time_2 = int(500*time_scale)
time_3 = int(700*time_scale)
time_4 = int(1000*time_scale)
action_groups_ato3 = [
      [#1[置中]
          {'id': 1, 'position': 300, 'time': time_4},
          {'id': 2, 'position': 500, 'time': time_4},
          {'id': 3, 'position': 300, 'time': time_4},
          {'id': 4, 'position': 900, 'time': time_4},
          {'id': 5, 'position': 700, 'time': time_4},
          {'id': 6, 'position': 500, 'time': time_4}
      ],
      [#2[a上張1]
          {'id': 1, 'position': 300, 'time': time_4},
          {'id': 2, 'position': 500, 'time': time_4},
          {'id': 3, 'position': 150, 'time': time_4},
          {'id': 4, 'position': 800, 'time': time_4},
          {'id': 5, 'position': 500, 'time': time_4},
          {'id': 6, 'position': 790, 'time': time_4}
      ],
      [#3[a上張2]
          {'id': 1, 'position': 300, 'time': time_1},
          {'id': 2, 'position': 500, 'time': time_1},
          {'id': 3, 'position': 150, 'time': time_1},
          {'id': 4, 'position': 800, 'time': time_1},
          {'id': 5, 'position': 450, 'time': time_1},
          {'id': 6, 'position': 790, 'time': time_1}
      ],
      [#4[a上張3]
          {'id': 1, 'position': 200, 'time': time_4},
          {'id': 2, 'position': 430, 'time': time_4},
          {'id': 3, 'position': 145, 'time': time_4},
          {'id': 4, 'position': 800, 'time': time_4},
          {'id': 5, 'position': 450, 'time': time_4},
          {'id': 6, 'position': 800, 'time': time_4}
      ],
      [#5[a上抓1]
          {'id': 1, 'position': 600, 'time': time_4},
          {'id': 2, 'position': 430, 'time': time_4},
          {'id': 3, 'position': 145, 'time': time_4},
          {'id': 4, 'position': 800, 'time': time_4},
          {'id': 5, 'position': 450, 'time': time_4},
          {'id': 6, 'position': 800, 'time': time_4}
      ],
      [#6[a上抓2]
          {'id': 1, 'position': 600, 'time': time_4},
          {'id': 2, 'position': 430, 'time': time_4},
          {'id': 3, 'position': 145, 'time': time_4},
          {'id': 4, 'position': 800, 'time': time_4},
          {'id': 5, 'position': 500, 'time': time_4},
          {'id': 6, 'position': 800, 'time': time_4}
      ],
      [#7[路上抓]
          {'id': 1, 'position': 600, 'time': time_4},
          {'id': 2, 'position': 500, 'time': time_4},
          {'id': 3, 'position': 170, 'time': time_4},
          {'id': 4, 'position': 800, 'time': time_4},
          {'id': 5, 'position': 480, 'time': time_4},
          {'id': 6, 'position': 360, 'time': time_4}
      ],
      [#8[3上抓1]
          {'id': 1, 'position': 600, 'time': time_3},
          {'id': 2, 'position': 500, 'time': time_3},
          {'id': 3, 'position': 180, 'time': time_3},
          {'id': 4, 'position': 550, 'time': time_3},
          {'id': 5, 'position': 300, 'time': time_3},
          {'id': 6, 'position': 360, 'time': time_3}
      ],
      [#9[3上抓2]
          {'id': 1, 'position': 600, 'time': time_2},
          {'id': 2, 'position': 500, 'time': time_2},
          {'id': 3, 'position': 180, 'time': time_2},
          {'id': 4, 'position': 550, 'time': time_2},
          {'id': 5, 'position': 275, 'time': time_2},
          {'id': 6, 'position': 360, 'time': time_2}
      ],
      [#10[1上放]
          {'id': 1, 'position': 300, 'time': time_4},
          {'id': 2, 'position': 500, 'time': time_4},
          {'id': 3, 'position': 200, 'time': time_4},
          {'id': 4, 'position': 550, 'time': time_4},
          {'id': 5, 'position': 275, 'time': time_4},
          {'id': 6, 'position': 360, 'time': time_4}
      ],
      [#11[置中]
          {'id': 1, 'position': 300, 'time': time_4},
          {'id': 2, 'position': 500, 'time': time_4},
          {'id': 3, 'position': 300, 'time': time_4},
          {'id': 4, 'position': 900, 'time': time_4},
          {'id': 5, 'position': 700, 'time': time_4},
          {'id': 6, 'position': 500, 'time': time_4}
      ]
  ]
# 反轉動作組順序，從1點移動回a點
action_groups_3toa = list(reversed(action_groups_ato3))



















