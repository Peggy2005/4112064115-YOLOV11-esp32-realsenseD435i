time_scale = 0.5
time_1 = int(400*time_scale)
time_2 = int(1600*time_scale)
time_3 = int(1500*time_scale)

action_groups_atob = [
      [#1[置中]
          {'id': 1, 'position': 300, 'time': time_2},
          {'id': 2, 'position': 500, 'time': time_2},
          {'id': 3, 'position': 300, 'time': time_2},
          {'id': 4, 'position': 900, 'time': time_2},
          {'id': 5, 'position': 700, 'time': time_2},
          {'id': 6, 'position': 500, 'time': time_2}
      ],
      [#2[a上張1]
          {'id': 1, 'position': 300, 'time': time_2},
          {'id': 2, 'position': 500, 'time': time_2},
          {'id': 3, 'position': 150, 'time': time_2},
          {'id': 4, 'position': 800, 'time': time_2},
          {'id': 5, 'position': 500, 'time': time_2},
          {'id': 6, 'position': 790, 'time': time_2}
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
          {'id': 1, 'position': 200, 'time': time_2},
          {'id': 2, 'position': 430, 'time': time_2},
          {'id': 3, 'position': 145, 'time': time_2},
          {'id': 4, 'position': 800, 'time': time_2},
          {'id': 5, 'position': 450, 'time': time_2},
          {'id': 6, 'position': 800, 'time': time_2}
      ],
      [#5[a上抓1]
          {'id': 1, 'position': 600, 'time': time_2},
          {'id': 2, 'position': 430, 'time': time_2},
          {'id': 3, 'position': 145, 'time': time_2},
          {'id': 4, 'position': 800, 'time': time_2},
          {'id': 5, 'position': 450, 'time': time_2},
          {'id': 6, 'position': 800, 'time': time_2}
      ],
      [#6[a上抓2]
          {'id': 1, 'position': 600, 'time': time_3},
          {'id': 2, 'position': 430, 'time': time_3},
          {'id': 3, 'position': 145, 'time': time_3},
          {'id': 4, 'position': 800, 'time': time_3},
          {'id': 5, 'position': 500, 'time': time_3},
          {'id': 6, 'position': 800, 'time': time_3}
      ],
      [#7[b上抓1]
          {'id': 1, 'position': 600, 'time': time_3},
          {'id': 2, 'position': 430, 'time': time_3},
          {'id': 3, 'position': 145, 'time': time_3},
          {'id': 4, 'position': 800, 'time': time_3},
          {'id': 5, 'position': 500, 'time': time_3},
          {'id': 6, 'position': 180, 'time': time_3}
      ],
      [#8[b上抓2]
          {'id': 1, 'position': 600, 'time': time_2},
          {'id': 2, 'position': 430, 'time': time_2},
          {'id': 3, 'position': 145, 'time': time_2},
          {'id': 4, 'position': 800, 'time': time_2},
          {'id': 5, 'position': 455, 'time': time_2},
          {'id': 6, 'position': 180, 'time': time_2}
      ],
      [#9[b上放1]
          {'id': 1, 'position': 300, 'time': time_2},
          {'id': 2, 'position': 430, 'time': time_2},
          {'id': 3, 'position': 145, 'time': time_2},
          {'id': 4, 'position': 800, 'time': time_2},
          {'id': 5, 'position': 450, 'time': time_2},
          {'id': 6, 'position': 180, 'time': time_2}
      ],
      [#9[b上放2]
          {'id': 1, 'position': 300, 'time': time_2},
          {'id': 2, 'position': 430, 'time': time_2},
          {'id': 3, 'position': 145, 'time': time_2},
          {'id': 4, 'position': 800, 'time': time_2},
          {'id': 5, 'position': 470, 'time': time_2},
          {'id': 6, 'position': 180, 'time': time_2}
      ],
      [#10[置中]
          {'id': 1, 'position': 300, 'time': time_2},
          {'id': 2, 'position': 500, 'time': time_2},
          {'id': 3, 'position': 300, 'time': time_2},
          {'id': 4, 'position': 900, 'time': time_2},
          {'id': 5, 'position': 700, 'time': time_2},
          {'id': 6, 'position': 500, 'time': time_2}
      ]
  ]
# 反轉動作組順序，從1點移動回a點
action_groups_btoa = list(reversed(action_groups_atob))











