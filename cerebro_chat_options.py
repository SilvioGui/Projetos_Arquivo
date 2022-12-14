import random


def outlier_phrase_campaign(coluna, type_alert, campaign, current_value, date1, color, varpercdelta, expected_value, sign, format_type, trigger, graph, outliers_over_time):
    if format_type == int:
        current_value = '{:0,}'.format(current_value)
        expected_value = '{:0,}'.format(expected_value)
    elif format_type == float:
        current_value = '{:0,.2f}'.format(current_value)
        expected_value = '{:0,.2f}'.format(expected_value)

    #critical situation phrases
    sign_text = {'+':{'green':{
                              'en':['greater','higher','better'],
                              'pt':['maior','mais alto','melhor'],
                              },
                      'red': {
                              'en':['greater','higher','worse'],
                              'pt':['maior','mais alto','pior'],
                              },
                      'blue':{
                              'en':['greater','higher'],
                              'pt':['maior','mais alto'],
                              },
                      },
                 '-':{'green':{'en':['lower','smaller','better'],
                              'pt':['menor','mais baixo','melhor'],
                              },
                      'red': {
                              'en':['lower','smaller','worse'],
                              'pt':['menor','mais baixo','pior'],
                              },
                      'blue':{
                              'en':['lower','smaller'],
                              'pt':['menor','mais baixo'],
                              },
                      }
                 }

    occurences_text = {'en':{0:'zero',
                             1:'first',
                             2:'second',
                             3:'third',
                             4:'fourth',
                             5:'fifth',
                             6:'sixth',
                             7:'seventh',
                             8:'eighth',
                             9:'nineth',
                             10:'tenth',
                             },
                       'pt':{0:'zero',
                             1:'primeira',
                             2:'segunda',
                             3:'terceira',
                             4:'quarta',
                             5:'quinta',
                             6:'sexta',
                             7:'s??tima',
                             8:'oitava',
                             9:'nona',
                             10:'d??cima',
                             },
                       }
                
    last_outs = 0
    if outliers_over_time[::-1][0] > 0:
        check_sign = 1
    else:
        check_sign = -1

    for term in outliers_over_time[::-1]:
        if term != check_sign:
            break
        else:
            last_outs += 1

    count_pos, count_neg = 0, 0
    for term in outliers_over_time:
        if term == 1:
            count_pos += 1
        if term == -1:
            count_neg += 1
        
    change_word = random.choice(sign_text[sign][color][language])
    outlier_dict1 = {'en':[
                        '<br><b>%s</b> value for the campaign <b>%s</b> was <b>%s</b> on <i>(%s)</i>. The percentage of difference is <span style="color:%s"><b>%s</b></span>, so this is critically %s than the expected value: <b>%s</b>.'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br><b>%s</b> data measured for campaign <b>%s</b> was <b>%s</b> on <i>(%s)</i>. The percentage of difference is <span style="color:%s"><b>%s</b></span> which makes it much %s than the expected value of <b>%s</b>.'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>I was expecting the campaign <b>%s %s</b> value to be around <b>%s</b>. The real value on <i>(%s)</i> was <b>%s</b> instead of it, so it actually ended up being <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(campaign, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>In normal conditions, the campaign <b>%s %s</b> should be around <b>%s</b>. Since the last value found <i>(%s)</i> was <b>%s</b>, this is really something worth to check. There is <span style="color:%s"><b>%s</b></span> of difference in the values, so it is much %s than normal.'
                        %(campaign, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br>Campaign <b>%s %s</b> values are normally around <b>%s</b>. Since I detected <b>%s</b> on <i>(%s)</i>, it is <span style="color:%s"><b>%s</b></span> %s, which is a lot %s than normal.'
                        %(campaign, coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, change_word),
                        '<br>Campaign <b>%s %s</b> value on <i>(%s)</i> has a great probability of being out of normality. Considering the other data points it should stay around <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(campaign, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I see a very unusual value for the campaign <b>%s %s</b> on <i>(%s)</i>. The proper number needs to be close to <b>%s</b>, but it\'s very far from that, it is <b>%s</b>. This means the new number is <span style="color:%s"><b>%s</b></span> %s.'
                        %(campaign, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        ],
                    'pt':[
                        '<br>O valor de <b>%s</b> encontrado para a campanha <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>. A diferen??a entre esse valor e o esperado ?? de <span style="color:%s"><b>%s</b></span>. Isso o torna muito %s do que o normal: <b>%s</b><br>'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor encontrado de <b>%s</b> para a campanha <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>. Esse valor ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado, o que o torna bastante fora do valor comum: <b>%s</b><br>'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor normal de <b>%s</b> na campanha <b>%s</b> deveria estar em torno de <b>%s</b>. Contudo, o valor em <i>(%s)</i> foi <b>%s</b>, o que ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, campaign, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Eu esperava que o valor de <b>%s</b> da campanha <b>%s</b> estivesse perto de <b>%s</b>. O valor foi bastante diferente em <i>(%s)</i>, foi de <b>%s</b> ao inv??s disso. Ent??o ele foi na verdade <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, campaign, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br>Os valores de <b>%s</b> na campanha <b>%s</b> geralmente ficam por volta de <b>%s</b>. Parece que h?? uma grande discrep??ncia, visto que eu encontrei <b>%s</b> no dia <i>(%s)</i>. Assim, o valor ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, campaign, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Existem grandes chances de que o n??mero <b>%s</b> n??o seja normal em <b>%s</b> para a campanha <b>%s</b>, ele foi encontrado no dia <i>(%s)</i>. Esse valor costumava ser muito diferente, perto de <b>%s</b>, o que indica um n??mero <span style="color:%s"><b>%s</b></span> %s do que deveria.'
                        %(current_value, coluna, campaign, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> da campanha <b>%s</b> est?? com um valor provavelmente anormal no dia <i>(%s)</i>. Considerando os outros pontos ele est?? bem longe do esperado, no patamar de <b>%s</b> ao inv??s de <b>%s</b>. Ent??o o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que deveria ser.'
                        %(coluna, campaign, date1, current_value, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu detectei uma grande distor????o no valor de <b>%s</b> da campanha <b>%s</b> no dia <i>(%s)</i>. Considerando os outros valores, eu acredito que um valor apropriado deveria ser bem diferente, por volta de <b>%s</b> no lugar de <b>%s</b>. Sendo assim, o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado.'
                        %(coluna, campaign, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu vejo um valor bastante fora do comum na campanha <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Um n??mero adequado devia ficar perto de <b>%s</b>, mas ele est?? muito longe disso, seu valor ?? <b>%s</b>. Isso significa que h?? um n??mero %s em <span style="color:%s"><b>%s</b></span>.'
                        %(coluna, campaign, date1, expected_value, current_value, change_word, color,'{:.2%}'.format(varpercdelta)),                       
                        ],
                }

    #not critical situation phrases
    outlier_dict2 = {'en':[
                        '<br><b>%s</b> value for the campaign <b>%s</b> was <b>%s</b> on <i>(%s)</i>, <span style="color:%s"><b>%s</b></span> %s than the expected value: <b>%s</b>.'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br><b>%s</b> data measured for campaign <b>%s</b> was <b>%s</b> on <i>(%s)</i>, which is <span style="color:%s"><b>%s</b></span> %s than the expected value of <b>%s</b>.'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                         '<br>I was expecting the campaign <b>%s %s</b> value to be around <b>%s</b>. The real value on <i>(%s)</i> was <b>%s</b> instead of it, so it actually was <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(campaign, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>In normal conditions, the campaign <b>%s %s</b> should be around <b>%s</b>. Since the last value found <i>(%s)</i> was <b>%s</b>, I believe this is something worth to check. There is <span style="color:%s"><b>%s</b></span> of difference in the values, so it is %s than normal.'
                        %(campaign, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br>Campaign <b>%s %s</b> values are normally around <b>%s</b>. Since I detected <b>%s</b> on <i>(%s)</i>, it is <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(campaign, coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Campaign <b>%s %s</b> value on <i>(%s)</i> is probably out of normality. Considering the other data points it should stay around <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(campaign, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I see an unusual value for campaign <b>%s %s</b> on <i>(%s)</i>. The proper number needs to be close to <b>%s</b>, not <b>%s</b>. This means the new number is <span style="color:%s"><b>%s</b></span> %s.'
                        %(campaign, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        ],
                'pt':[
                        '<br>O valor de <b>%s</b> encontrado para a campanha <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>, que ?? <span style="color:%s"><b>%s</b></span> %s do que o valor esperado: <b>%s</b><br>'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor encontrado de <b>%s</b> para a campanha <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>, que ?? <span style="color:%s"><b>%s</b></span> %s do que o valor esperado: <b>%s</b><br>'
                        %(coluna, campaign, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor normal de <b>%s</b> na campanha <b>%s</b> deveria estar em torno de <b>%s</b>. Contudo, o valor em <i>(%s)</i> foi <b>%s</b>, o que ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, campaign, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Eu esperava que o valor de <b>%s</b> da campanha <b>%s</b> estivesse perto de <b>%s</b>. O valor real em <i>(%s)</i> foi de <b>%s</b> ao inv??s disso. Ent??o ele foi na verdade <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, campaign, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Em condi????es normais <b>%s</b> em <b>%s</b> deveria estar em torno de <b>%s</b>. Como o ??ltimo valor encontrado em <i>(%s)</i> foi <b>%s</b>, eu acredito que valha a pena se atentar a isso. Existe um percentual de <span style="color:%s"><b>%s</b></span> de diferen??a nos valores.'
                        %(coluna, campaign, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta)),
                        '<br>Os valores de <b>%s</b> na campanha <b>%s</b> geralmente ficam por volta de <b>%s</b>. Visto que eu encontrei <b>%s</b> no dia <i>(%s)</i>, temos um valor <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, campaign, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Existem grandes chances de que o n??mero <b>%s</b> n??o seja normal para a campanha <b>%s</b> em <b>%s</b>, ele foi encontrado no dia <i>(%s)</i>. Esse valor costuma ficar perto de <b>%s</b>, o que faz com que o n??mero seja <span style="color:%s"><b>%s</b></span> %s do que deveria.'
                        %(current_value, campaign, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> da campanha <b>%s</b> est?? com um valor provavelmente anormal no dia <i>(%s)</i>. Considerando os outros pontos ele deveria estar perto de <b>%s</b> ao inv??s de <b>%s</b>. Ent??o o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que deveria ser.'
                        %(coluna, campaign, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu detectei uma distor????o no valor de <b>%s</b> na campanha <b>%s</b> no dia <i>(%s)</i>. Considerando os outros valores, eu acredito que um valor apropriado deveria ser <b>%s</b> no lugar de <b>%s</b>. Sendo assim, o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado.'
                        %(coluna, campaign, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu vejo um valor fora do comum na campanha <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Um n??mero adequado devia ficar perto de <b>%s</b>, n??o perto de <b>%s</b>. Isso significa que h?? um n??mero %s em <span style="color:%s"><b>%s</b></span>.'
                        %(coluna, campaign, date1, expected_value, current_value, change_word, color,'{:.2%}'.format(varpercdelta)),                       
                        ],
            }

    outlier_dict_graph1 = {'en':[' You can see with the graph that the difference between this last value and the others is very high!',
                                ' The big discrepance of this value and the others is visible below.',
                                ' I thought it would be easier to show how much this value is far from the others in the following image',
                                ' Since this distortion is huge, perhaps you should see it in the graph below.',
                                ' Take a look in the picture so you can see the big difference between them.',
                                ' This huge difference between this point and the others is shown in the graph, take a look.',
                                ' The value is clearly off the limits that define the normal values in the graph.',
                                ],
                         'pt':[ ' Voc?? pode ver pelo gr??fico que a diferen??a entre esse ??ltimo valor e os outros ?? muito alta!',
                                ' A grande discrep??ncia desse valor ?? vis??vel abaixo.',
                                ' Eu achei que seria mais simples mostrar o quanto esse ponto se distancia dos outros na imagem a seguir.',
                                ' Visto que essa distor????o ?? enorme, talvez voc?? deva v??-la no gr??fico abaixo.',
                                ' Veja a figura abaixo para que voc?? possa ver a grande diferen??a entre eles.',
                                ' Existe uma grande diferen??a entre esse ponto e os outros, d?? uma olhada.',
                                ' O valor est?? claramente fora dos limites de normalidade pelo gr??fico.',
                                ],
                         }

    outlier_dict_graph2 = {'en':[' You can see the difference between this last value and the others below.',
                                ' Check the graph below to the see this behavior.',
                                ' I believe the image can show this clearly.',
                                ' Take a look in the following data plot.',
                                ' I drew a graph to help you visualize this issue.',
                                ' I made a draft from my analysis, I hope you can see the issue.',
                                ' I considered the situation detailed in the image to determine this is not a normal value.',
                                ' The red point in graph shows the difference between this value and the other ones.',
                                ' It is easy to see the difference from this value and the others below.',
                                ' It is easy to see this situation with the graph.',
                                ' Perhaps it\'s better to see this with the graph below.',
                                ' I think you can see pretty well the data point appearing off the limits in the following picture.',
                                ' The limits considered to be normal are shown in the picture below.',
                                ],
                         'pt':[ ' ?? poss??vel ver a diferen??a entre esse ??ltimo valor e os outros abaixo.',
                                ' Veja esse comportamento no gr??fico abaixo.',
                                ' Eu acredito que a imagem abaixo pode mostrar isso mais claramente.',
                                ' Veja isso na plotagem dos dados seguinte.',
                                ' Eu fiz um gr??fico para ajudar a visualizar isso.',
                                ' Eu fiz um esbo??o da minha an??lise abaixo para ajudar a visualizar essa quest??o.',
                                ' Eu considerei a situa????o detalhada na imagem abaixo para determinar que o valor est?? fora dos padr??es.',
                                ' O ponto vermelho no gr??fico mostra a diferen??a entre esse valor e os outros.',
                                ' ?? f??cil ver a diferen??a entre os valores, d?? uma olhada.',
                                ' ?? simples de ver essa situa????o com um gr??fico.',
                                ' Talvez seja melhor ver isso com o gr??fico abaixo.',
                                ' Eu acho que d?? para ver com clareza como o ??ltimo ponto aparece fora dos limites na figura a seguir.',
                                ' Os limites considerados normais est??o ilustrados na imagem abaixo.',
                                ],
                         }


    directions_dict = {'high-value':{
                    'en':['Aparently, <b>%s</b> value is high in the campaign <b>%s</b>.' %(coluna, campaign),
                          'The campaign <b>%s</b> certainly has a high value in <b>%s</b>.' %(campaign, coluna),
                          'It is recommended to pay attention to the campaign <b>%s</b>, because it shows big values in <b>%s</b>.' %(campaign, coluna),
                          'I see a value of <span style="color:%s"><b>%s</b></span> for campaign <b>%s %s</b>. It\'s quite a high value.' %(color, current_value, campaign, coluna),                        
                          ],
                    'pt':['Aparentemente o valor de <b>%s</b> est?? alto na campanha <b>%s</b>.' %(coluna, campaign),
                          'Certamente a campanha <b>%s</b> tem um valor consideravelmente alto em <b>%s</b>.' %(campaign, coluna),
                          '?? bom estar atento ?? campanha <b>%s</b>, pois ela est?? com valores altos em <b>%s</b>.' %(campaign, coluna),                        
                          'Vejo um valor de <span style="color:%s"><b>%s</b></span> para <b>%s</b> da campanha <b>%s</b>. ?? um valor relativamente alto.' %(color, current_value, coluna, campaign),                        
                          ],
                    },

                       'low-value':{
                    'en':['Aparently, <b>%s</b> value is low in the campaign <b>%s</b>.' %(coluna, campaign),
                          'The campaign <b>%s</b> certainly has a low value in <b>%s</b>.' %(campaign, coluna),
                          'It is recommended to pay attention to the campaign <b>%s</b>, because it shows small values in <b>%s</b>.' %(campaign, coluna),
                          'I see a value of <span style="color:%s"><b>%s</b></span> for campaign <b>%s %s</b>. It\'s quite a low value.' %(color, current_value, campaign, coluna),                        
                          ],
                    'pt':['Aparentemente o valor de <b>%s</b> est?? baixo na campanha <b>%s</b>.' %(coluna, campaign),
                          'Certamente a campanha <b>%s</b> tem um valor consideravelmente baixo em <b>%s</b>.' %(campaign, coluna),
                          '?? bom estar atento ?? campanha <b>%s</b>, pois ela est?? com valores baixos em <b>%s</b>.' %(campaign, coluna),                        
                          'Vejo um valor de <span style="color:%s"><b>%s</b></span> para <b>%s</b> da campanha <b>%s</b>. ?? um valor relativamente pequeno.' %(color, current_value, coluna, campaign),                        
                          ],
                    },
                }

    campaign_comments = {'green':{
                                 'en':[' This shows the campaign is being effective.',
                                       ' We can see the campaign numbers are positive',
                                       ' The investiment is being done in good conditions',
                                       ' The investiments made are having good results',
                                       ],
                                 'pt':[' Isso mostra que a campanha est?? sendo efetiva.',
                                       ' Percebe-se que os n??meros da campanha s??o positivos',
                                       ' O investimento est?? sendo feito em boas condi????es',
                                       ' O investimento feito est?? tendo bons resultados',
                                       ],
                              },
                         'red':{
                                 'en':[' This shows the campaign could be more effective.',
                                       ' We can see the campaign numbers are negative',
                                       ' The investiment could have some improvements',
                                       ' The investiments made aren\'t having the best results',
                                       ],
                                 'pt':[' Isso mostra que a campanha poderia ser mais efetiva.',
                                       ' Percebe-se que os n??meros da campanha n??o est??o t??o bons',
                                       ' O investimento sendo feito pode melhorar',
                                       ' O investimento feito n??o est?? tendo os melhores resultados',
                                       ],
                              },
                         }


    recurrent_dict = {'en':['<br>This is the %s time we are facing this behavior.' %occurences_text[language][last_outs],
                            '<br>This is the %s value I detected with the same behavior.' %occurences_text[language][last_outs],
                            '<br>As you can see, this is not the first time this happens.',
                            '<br>The last %s points are going through this.' %str(last_outs),
                            '<br>This behavior is repeating for a while, it is important to know if everything is fine.',
                            '<br>This is not the first time it happens with this KPI, actually it is the %s time.' %occurences_text[language][last_outs],
                            '<br>Notice this is happening for the %s time.' %occurences_text[language][last_outs],
                            '<br>We have now the last %s occurences in this situation.' %str(last_outs),
                            '<br>The last %s values are outliers with the same behavior.' %str(last_outs),
                            '<br>This is the %s outlier found in this kind of analysis.' %occurences_text[language][last_outs],
                                ],
                     'pt':[ '<br>Essa ?? a %s vez que esse comportamento ocorre.' %occurences_text[language][last_outs],
                            '<br>Os valores tem o mesmo comportamento pela %s vez.' %occurences_text[language][last_outs],
                            '<br>Esse j?? ?? o %s valor encontrado com esse comportamento.' %occurences_text[language][last_outs].replace("a","o"),
                            '<br>Como voc?? pode ver, n??o ?? a primeira vez que isso acontece.',
                            '<br>Os ??ltimos %s pontos est??o passando por isso.' %str(last_outs),
                            '<br>Essa situa????o tem se repetido por algum tempo, talvez seja sentato verificar se est?? tudo certo.',
                            '<br>N??o ?? a primeira vez que isso ocorre com esse KPI, na verdade ?? a %s vez.' %occurences_text[language][last_outs],
                            '<br>Repare que isso j?? aconteceu pela %s vez.' %occurences_text[language][last_outs],
                            '<br>N??s temos agora as ??ltimas %s ocorr??ncias desse jeito.' %str(last_outs),
                            '<br>Os ??ltimos %s valores s??o outliers com mesmo comportamento.' %str(last_outs),
                            '<br>?? o %s outlier encontrado nesse tipo de an??lise.' %occurences_text[language][last_outs].replace("a","o"),
                                ],
                         }

    enthusiasm_dict = {'good':{'en':['<br>I think you will like the numbers I have for you!'],
                               'pt':[ '<br>D?? uma olhada nos n??meros abaixo, est??o bem positivos!'],
                         },
                       'bad':{'en':['<br>I think you should look closely to the numbers I have for you! They are not good at all!'],
                               'pt':[ '<br>D?? uma olhada com aten????o nos n??meros abaixo! Eles n??o s??o nada positivos!'],
                         },
                       }



    if type_alert[3] == True and trigger == 'outlier-by-sample':
        text = random.choice(outlier_dict1[language])
    elif type_alert[3] == False and trigger == 'outlier-by-sample':
        text = random.choice(outlier_dict2[language])
    elif trigger == 'high-value' or trigger == 'low-value':
        text = random.choice(directions_dict[trigger][language])

    if random.randint(1,100) > 75:
        text += random.choice(campaign_comments[color][language])

    critical_condition = False   
    if graph == 'yes' and type_alert[3] == True:
        critical_condition = True
    elif graph == 'yes' and type_alert[3] == False:
        critical_condition = False

    if random.randint(1,100) > 60 and graph == 'yes' and trigger == 'outlier-by-sample' and critical_condition == True:
        text += random.choice(outlier_dict_graph1[language])
    elif random.randint(1,100) > 60 and graph == 'yes' and trigger == 'outlier-by-sample':
        text += random.choice(outlier_dict_graph2[language])

    if graph == 'yes' and last_outs > 1:
        recurrent_condition = True
    else:
        recurrent_condition = False

    if recurrent_condition == True and random.randint(1,100) > 60 and trigger == 'outlier-by-sample':
        text += random.choice(recurrent_dict[language])

    return text

def outlier_phrase(coluna, type_alert, traffic_type, current_value, date1, color, varpercdelta, expected_value, sign, format_type, dimension_condition, graph, outliers_over_time):
    if format_type == int:
        current_value = '{:0,}'.format(current_value)
        expected_value = '{:0,}'.format(expected_value)
    elif format_type == float:
        current_value = '{:0,.2f}'.format(current_value)
        expected_value = '{:0,.2f}'.format(expected_value)

    #critical situation phrases
    sign_text = {'+':{'green':{
                              'en':['greater','higher','better'],
                              'pt':['maior','mais alto','melhor'],
                              },
                      'red': {
                              'en':['greater','higher','worse'],
                              'pt':['maior','mais alto','pior'],
                              },
                      'blue':{
                              'en':['greater','higher'],
                              'pt':['maior','mais alto'],
                              },
                      },
                 '-':{'green':{'en':['lower','smaller','better'],
                              'pt':['menor','mais baixo','melhor'],
                              },
                      'red': {
                              'en':['lower','smaller','worse'],
                              'pt':['menor','mais baixo','pior'],
                              },
                      'blue':{
                              'en':['lower','smaller'],
                              'pt':['menor','mais baixo'],
                              },
                      }
                 }

    occurences_text = {'en':{1:'first',
                             2:'second',
                             3:'third',
                             4:'fourth',
                             5:'fifth',
                             },
                       'pt':{1:'primeira',
                             2:'segunda',
                             3:'terceira',
                             4:'quarta',
                             5:'quinta',
                             },
                       }
                
    last_outs = 0
    if outliers_over_time[::-1][0] > 0:
        check_sign = 1
    else:
        check_sign = -1

    for term in outliers_over_time[::-1]:
        if term != check_sign:
            break
        else:
            last_outs += 1

    count_pos, count_neg = 0, 0
    for term in outliers_over_time:
        if term == 1:
            count_pos += 1
        if term == -1:
            count_neg += 1
        
    change_word = random.choice(sign_text[sign][color][language])
    outlier_dict1 = {
                    'en':{'dimension_on':
                        [
                        '<br><b>%s</b> value for <b>%s</b> was <b>%s</b> on <i>(%s)</i>. The percentage of difference is <span style="color:%s"><b>%s</b></span>, so this is critically %s than the expected value: <b>%s</b>.'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br><b>%s</b> data measured for %s was <b>%s</b> on <i>(%s)</i>. The percentage of difference is <span style="color:%s"><b>%s</b></span> which makes it much %s than the expected value of <b>%s</b>.'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>The normal value for <b>%s %s</b> is supposed to be around <b>%s</b>. The value detected on <i>(%s)</i> was much %s, it was <b>%s</b>, which is <span style="color:%s"><b>%s</b></span> than normal.'
                        %(traffic_type, coluna, expected_value, date1, change_word, current_value, color, '{:.2%}'.format(varpercdelta)),
                        '<br>I was expecting <b>%s %s</b> value to be around <b>%s</b>. The real value on <i>(%s)</i> was <b>%s</b> instead of it, so it actually ended up being <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(traffic_type, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>In normal conditions <b>%s %s</b> should be around <b>%s</b>. Since the last value found <i>(%s)</i> was <b>%s</b>, this is really something worth to check. There is <span style="color:%s"><b>%s</b></span> of difference in the values, so it is much %s than normal.'
                        %(traffic_type, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s %s</b> values are normally around <b>%s</b>. Since I detected <b>%s</b> on <i>(%s)</i>, it is <span style="color:%s"><b>%s</b></span> %s, which is a lot %s than normal.'
                        %(traffic_type, coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, change_word),
                        '<br>There are very big chances that <b>%s</b> is not normal for <b>%s %s</b>, it was found on <i>(%s)</i>. This value is usually near <b>%s</b>, so I think the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(current_value, traffic_type, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s %s</b> value on <i>(%s)</i> has a great probability of being out of normality. Considering the other data points it should stay around <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(traffic_type, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I detected a very high distortion on <b>%s %s</b> value on <i>(%s)</i>. Considering the values from the other points, I believe a proper value should be <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than the expected.'
                        %(traffic_type, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I see a very unusual value for <b>%s %s</b> on <i>(%s)</i>. The proper number needs to be close to <b>%s</b>, but it\'s very far from that, it is <b>%s</b>. This means the new number is <span style="color:%s"><b>%s</b></span> %s.'
                        %(traffic_type, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        ],
                    'dimension_off':
                        [
                        '<br><b>%s</b> value was <b>%s</b> on <i>(%s)</i>. The percentage of difference is <span style="color:%s"><b>%s</b></span>, so this is critically %s than the expected value: <b>%s</b>.'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br><b>%s</b> data measured was <b>%s</b> on <i>(%s)</i>. The percentage of difference is <span style="color:%s"><b>%s</b></span> which makes it much %s than the expected value of <b>%s</b>.'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>The normal value for <b>%s</b> is supposed to be around <b>%s</b>. The value detected on <i>(%s)</i> was much %s, it was <b>%s</b>, which is <span style="color:%s"><b>%s</b></span> than normal.'
                        %(coluna, expected_value, date1, change_word, current_value, color, '{:.2%}'.format(varpercdelta)),
                        '<br>I was expecting <b>%s</b> value to be around <b>%s</b>. The real value on <i>(%s)</i> was <b>%s</b> instead of it, so it actually ended up being <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>In normal conditions <b>%s</b> should be around <b>%s</b>. Since the last value found <i>(%s)</i> was <b>%s</b>, this is really something worth to check. There is <span style="color:%s"><b>%s</b></span> of difference in the values, so it is %s than normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> values are normally around <b>%s</b>. Since I detected <b>%s</b> on <i>(%s)</i>, it is <span style="color:%s"><b>%s</b></span> %s, which is a lot %s than normal.'
                        %(coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, change_word),
                        '<br>There are very big chances that <b>%s</b> is not normal for <b>%s</b>, it was found on <i>(%s)</i>. This value is usually near <b>%s</b>, so I think the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(current_value, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> value on <i>(%s)</i> has a great probability of being out of normality. Considering the other data points it should stay around <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I detected a very high distortion on <b>%s</b> value on <i>(%s)</i>. Considering the values from the other points, I believe a proper value should be <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than the expected.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I see a very unusual value for <b>%s</b> on <i>(%s)</i>. The proper number needs to be close to <b>%s</b>, but it\'s very far from that, it is <b>%s</b>. This means the new number is <span style="color:%s"><b>%s</b></span> %s.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        ],
                         },
                    'pt':{'dimension_on':
                        [
                        '<br>O valor de <b>%s</b> encontrado para <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>. A diferen??a entre esse valor e o esperado ?? de <span style="color:%s"><b>%s</b></span>. Isso o torna muito %s do que o normal: <b>%s</b><br>'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor encontrado de <b>%s</b> para %s foi <b>%s</b> no dia <i>(%s)</i>. Esse valor ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado, o que o torna bastante fora do valor comum: <b>%s</b><br>'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor normal de <b>%s</b> em <b>%s</b> deveria estar em torno de <b>%s</b>. Contudo, o valor em <i>(%s)</i> foi <b>%s</b>, o que ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, traffic_type, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Eu esperava que o valor de <b>%s</b> em <b>%s</b> estivesse perto de <b>%s</b>. O valor foi bastante diferente em <i>(%s)</i>, foi de <b>%s</b> ao inv??s disso. Ent??o ele foi na verdade <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, traffic_type, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Em condi????es normais <b>%s</b> em <b>%s</b> deveria estar em torno de <b>%s</b>. Como o ??ltimo valor encontrado em <i>(%s)</i> foi <b>%s</b>, eu acredito que valha a pena se atentar a isso. Existe um percentual de <span style="color:%s"><b>%s</b></span> de diferen??a nos valores, ent??o ele foi realmente %s do que o normal.'
                        %(coluna, traffic_type, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br>Os valores de <b>%s</b> em <b>%s</b> geralmente ficam por volta de <b>%s</b>. Parece que h?? uma grande discrep??ncia, visto que eu encontrei <b>%s</b> no dia <i>(%s)</i>. Assim, o valor ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, traffic_type, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Existem grandes chances de que o n??mero <b>%s</b> n??o seja normal para <b>%s</b> em <b>%s</b>, ele foi encontrado no dia <i>(%s)</i>. Esse valor costumava ser muito diferente, perto de <b>%s</b>, o que indica um n??mero <span style="color:%s"><b>%s</b></span> %s do que deveria.'
                        %(current_value, traffic_type, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> em <b>%s</b> est?? com um valor provavelmente anormal no dia <i>(%s)</i>. Considerando os outros pontos ele est?? bem longe do esperado, no patamar de <b>%s</b> ao inv??s de <b>%s</b>. Ent??o o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que deveria ser.'
                        %(coluna, traffic_type, date1, current_value, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu detectei uma grande distor????o no valor de <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Considerando os outros valores, eu acredito que um valor apropriado deveria ser bem diferente, por volta de <b>%s</b> no lugar de <b>%s</b>. Sendo assim, o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado.'
                        %(coluna, traffic_type, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu vejo um valor bastante fora do comum em <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Um n??mero adequado devia ficar perto de <b>%s</b>, mas ele est?? muito longe disso, seu valor ?? <b>%s</b>. Isso significa que h?? um n??mero %s em <span style="color:%s"><b>%s</b></span>.'
                        %(coluna, traffic_type, date1, expected_value, current_value, change_word, color,'{:.2%}'.format(varpercdelta)),                       
                        ],
                     'dimension_off':
                        [
                        '<br>O valor de <b>%s</b> encontrado foi <b>%s</b> no dia <i>(%s)</i>. A diferen??a entre esse valor e o esperado ?? de <span style="color:%s"><b>%s</b></span>. Isso o torna muito %s do que o normal: <b>%s</b><br>'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor encontrado de <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>. Esse valor ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado, o que o torna bastante fora do valor comum: <b>%s</b><br>'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor normal de <b>%s</b> deveria estar em torno de <b>%s</b>. Contudo, o valor em <i>(%s)</i> foi <b>%s</b>, o que ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Eu esperava que o valor de <b>%s</b> estivesse perto de <b>%s</b>. O valor foi bastante diferente em <i>(%s)</i>, foi de <b>%s</b> ao inv??s disso. Ent??o ele foi na verdade <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Em condi????es normais <b>%s</b> deveria estar em torno de <b>%s</b>. Como o ??ltimo valor encontrado em <i>(%s)</i> foi <b>%s</b>, eu acredito que valha a pena se atentar a isso. Existe um percentual de <span style="color:%s"><b>%s</b></span> de diferen??a nos valores, ent??o ele foi realmente %s do que o normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br>Os valores de <b>%s</b> geralmente ficam por volta de <b>%s</b>. Parece que h?? uma grande discrep??ncia, visto que eu encontrei <b>%s</b> no dia <i>(%s)</i>. Assim, o valor ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Existem grandes chances de que o n??mero <b>%s</b> n??o seja normal para <b>%s</b>, ele foi encontrado no dia <i>(%s)</i>. Esse valor costumava ser muito diferente, perto de <b>%s</b>, o que indica um n??mero <span style="color:%s"><b>%s</b></span> %s do que deveria.'
                        %(current_value, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> est?? com um valor provavelmente anormal no dia <i>(%s)</i>. Considerando os outros pontos ele deveria estar bem longe disso, no patamar de <b>%s</b> ao inv??s de <b>%s</b>. Ent??o o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que deveria ser.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu detectei uma grande distor????o no valor de <b>%s</b> no dia <i>(%s)</i>. Considerando os outros valores, eu acredito que um valor apropriado deveria ser bem diferente, por volta de <b>%s</b> no lugar de <b>%s</b>. Sendo assim, o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu vejo um valor bastante fora do comum em <b>%s</b> no dia <i>(%s)</i>. Um n??mero adequado devia ficar perto de <b>%s</b>, mas ele est?? muito longe disso, seu valor ?? <b>%s</b>. Isso significa que h?? um n??mero %s em <span style="color:%s"><b>%s</b></span>.'
                        %(coluna, date1, expected_value, current_value, change_word, color,'{:.2%}'.format(varpercdelta)),                       
                        ],
                        }
                 }

    #not critical situation phrases
    outlier_dict2 = {
                'en':{'dimension_on':
                        [
                        '<br><b>%s</b> value for <b>%s</b> was <b>%s</b> on <i>(%s)</i>, <span style="color:%s"><b>%s</b></span> %s than the expected value: <b>%s</b>.'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br><b>%s</b> data measured for %s was <b>%s</b> on <i>(%s)</i>, which is <span style="color:%s"><b>%s</b></span> %s than the expected value of <b>%s</b>.'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>The normal value for <b>%s %s</b> is supposed to be around <b>%s</b>. The value on <i>(%s)</i> was <b>%s</b>, which is <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(traffic_type, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>I was expecting <b>%s %s</b> value to be around <b>%s</b>. The real value on <i>(%s)</i> was <b>%s</b> instead of it, so it actually was <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(traffic_type, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>In normal conditions <b>%s %s</b> should be around <b>%s</b>. Since the last value found <i>(%s)</i> was <b>%s</b>, I believe this is something worth to check. There is <span style="color:%s"><b>%s</b></span> of difference in the values, so it is %s than normal.'
                        %(traffic_type, coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s %s</b> values are normally around <b>%s</b>. Since I detected <b>%s</b> on <i>(%s)</i>, it is <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(traffic_type, coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>There are great chances that the value <b>%s</b> is not normal for <b>%s %s</b>, it was found on <i>(%s)</i>. This value is usually near <b>%s</b>, so the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(current_value, traffic_type, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s %s</b> value on <i>(%s)</i> is probably out of normality. Considering the other data points it should stay around <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(traffic_type, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I detected a distortion on <b>%s %s</b> value on <i>(%s)</i>. Considering the values from the other points, I believe a proper value should be <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than the expected.'
                        %(traffic_type, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I see an unusual value for <b>%s %s</b> on <i>(%s)</i>. The proper number needs to be close to <b>%s</b>, not <b>%s</b>. This means the new number is <span style="color:%s"><b>%s</b></span> %s.'
                        %(traffic_type, coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        ],
                    'dimension_off':
                        [
                        '<br><b>%s</b> value was <b>%s</b> on <i>(%s)</i>, <span style="color:%s"><b>%s</b></span> %s than the expected value: <b>%s</b>.'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br><b>%s</b> data measured was <b>%s</b> on <i>(%s)</i>, which is <span style="color:%s"><b>%s</b></span> %s than the expected value of <b>%s</b>.'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>The normal value for <b>%s</b> is supposed to be around <b>%s</b>. The value on <i>(%s)</i> was <b>%s</b>, which is <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>I was expecting <b>%s</b> value to be around <b>%s</b>. The real value on <i>(%s)</i> was <b>%s</b> instead of it, so it actually was <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>In normal conditions <b>%s</b> should be around <b>%s</b>. Since the last value found <i>(%s)</i> was <b>%s</b>, I believe this is something worth to check. There is <span style="color:%s"><b>%s</b></span> of difference in the values, so it is %s than normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> values are normally around <b>%s</b>. Since I detected <b>%s</b> on <i>(%s)</i>, it is <span style="color:%s"><b>%s</b></span> %s than normal.'
                        %(coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>There are great chances that the value <b>%s</b> is not normal for <b>%s</b>, it was found on <i>(%s)</i>. This value is usually near <b>%s</b>, so the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(current_value, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> value on <i>(%s)</i> is probably out of normality. Considering the other data points it should stay around <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than it should be.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I detected a distortion on <b>%s</b> value on <i>(%s)</i>. Considering the values from the other points, I believe a proper value should be <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than the expected.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I detected a distortion on <b>%s</b> value on <i>(%s)</i>. Considering the values from the other points, I believe a proper value should be <b>%s</b> instead of <b>%s</b>. So the number is <span style="color:%s"><b>%s</b></span> %s than the expected.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>I see an unusual value for <b>%s</b> on <i>(%s)</i>. The proper number needs to be close to <b>%s</b>, not <b>%s</b>. This means the new number is <span style="color:%s"><b>%s</b></span> %s.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        ],
                     },
                'pt':{'dimension_on':
                        [
                        '<br>O valor de <b>%s</b> encontrado para <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>, que ?? <span style="color:%s"><b>%s</b></span> %s do que o valor esperado: <b>%s</b><br>'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor encontrado de <b>%s</b> para <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>, que ?? <span style="color:%s"><b>%s</b></span> %s do que o valor esperado: <b>%s</b><br>'
                        %(coluna, traffic_type, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor normal de <b>%s</b> em <b>%s</b> deveria estar em torno de <b>%s</b>. Contudo, o valor em <i>(%s)</i> foi <b>%s</b>, o que ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, traffic_type, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Eu esperava que o valor de <b>%s</b> em <b>%s</b> estivesse perto de <b>%s</b>. O valor real em <i>(%s)</i> foi de <b>%s</b> ao inv??s disso. Ent??o ele foi na verdade <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, traffic_type, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Em condi????es normais <b>%s</b> em <b>%s</b> deveria estar em torno de <b>%s</b>. Como o ??ltimo valor encontrado em <i>(%s)</i> foi <b>%s</b>, eu acredito que valha a pena se atentar a isso. Existe um percentual de <span style="color:%s"><b>%s</b></span> de diferen??a nos valores.'
                        %(coluna, traffic_type, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta)),
                        '<br>Os valores de <b>%s</b> em <b>%s</b> geralmente ficam por volta de <b>%s</b>. Visto que eu encontrei <b>%s</b> no dia <i>(%s)</i>, temos um valor <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, traffic_type, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Existem grandes chances de que o n??mero <b>%s</b> n??o seja normal para <b>%s</b> em <b>%s</b>, ele foi encontrado no dia <i>(%s)</i>. Esse valor costuma ficar perto de <b>%s</b>, o que faz com que o n??mero seja <span style="color:%s"><b>%s</b></span> %s do que deveria.'
                        %(current_value, coluna, traffic_type, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> em <b>%s</b> est?? com um valor provavelmente anormal no dia <i>(%s)</i>. Considerando os outros pontos ele deveria estar perto de <b>%s</b> ao inv??s de <b>%s</b>. Ent??o o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que deveria ser.'
                        %(coluna, traffic_type, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu detectei uma distor????o no valor de <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Considerando os outros valores, eu acredito que um valor apropriado deveria ser <b>%s</b> no lugar de <b>%s</b>. Sendo assim, o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado.'
                        %(coluna, traffic_type, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu vejo um valor fora do comum em <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Um n??mero adequado devia ficar perto de <b>%s</b>, n??o perto de <b>%s</b>. Isso significa que h?? um n??mero %s em <span style="color:%s"><b>%s</b></span>.'
                        %(coluna, traffic_type, date1, expected_value, current_value, change_word, color,'{:.2%}'.format(varpercdelta)),                       
                        ],
                     'dimension_off':
                        [
                        '<br>O valor de <b>%s</b> encontrado foi <b>%s</b> no dia <i>(%s)</i>, que ?? <span style="color:%s"><b>%s</b></span> %s do que o valor esperado: <b>%s</b><br>'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor encontrado de <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>, que ?? <span style="color:%s"><b>%s</b></span> %s do que o valor esperado: <b>%s</b><br>'
                        %(coluna, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word, expected_value),
                        '<br>O valor normal de <b>%s</b> deveria estar em torno de <b>%s</b>. Contudo, o valor em <i>(%s)</i> foi <b>%s</b>, o que ?? <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Eu esperava que o valor de <b>%s</b> estivesse perto de <b>%s</b>. O valor real em <i>(%s)</i> foi de <b>%s</b> ao inv??s disso. Ent??o ele foi na verdade <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta), change_word),
                         '<br>Em condi????es normais <b>%s</b> deveria estar em torno de <b>%s</b>. Como o ??ltimo valor encontrado em <i>(%s)</i> foi <b>%s</b>, eu acredito que valha a pena se atentar a isso. Existe um percentual de <span style="color:%s"><b>%s</b></span> de diferen??a nos valores.'
                        %(coluna, expected_value, date1, current_value, color, '{:.2%}'.format(varpercdelta)),
                        '<br>Os valores de <b>%s</b> geralmente ficam por volta de <b>%s</b>. Visto que eu encontrei <b>%s</b> no dia <i>(%s)</i>, temos um valor <span style="color:%s"><b>%s</b></span> %s do que o normal.'
                        %(coluna, expected_value, current_value, date1, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Existem grandes chances de que o n??mero <b>%s</b> n??o seja normal para <b>%s</b>, ele foi encontrado no dia <i>(%s)</i>. Esse valor costuma ficar perto de <b>%s</b>, o que faz com que o n??mero seja <span style="color:%s"><b>%s</b></span> %s do que deveria.'
                        %(current_value, coluna, date1, expected_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br><b>%s</b> est?? com um valor provavelmente anormal no dia <i>(%s)</i>. Considerando os outros pontos ele deveria estar perto de <b>%s</b> ao inv??s de <b>%s</b>. Ent??o o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que deveria ser.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu detectei uma distor????o no valor de <b>%s</b> no dia <i>(%s)</i>. Considerando os outros valores, eu acredito que um valor apropriado deveria ser <b>%s</b> no lugar de <b>%s</b>. Sendo assim, o n??mero ?? <span style="color:%s"><b>%s</b></span> %s do que o esperado.'
                        %(coluna, date1, expected_value, current_value, color,'{:.2%}'.format(varpercdelta), change_word),
                        '<br>Eu vejo um valor fora do comum em <b>%s</b> no dia <i>(%s)</i>. Um n??mero adequado devia ficar perto de <b>%s</b>, n??o perto de <b>%s</b>. Isso significa que h?? um n??mero %s em <span style="color:%s"><b>%s</b></span>.'
                        %(coluna, date1, expected_value, current_value, change_word, color,'{:.2%}'.format(varpercdelta)),                       
                        ],
                     }
                }

    outlier_dict_graph1 = {'en':[' You can see with the graph that the difference between this last value and the others is very high!',
                                ' The big discrepance of this value and the others is visible below.',
                                ' I thought it would be easier to show how much this value is far from the others in the following image',
                                ' Since this distortion is huge, perhaps you should see it in the graph below.',
                                ' Take a look in the picture so you can see the big difference between them.',
                                ' This huge difference between this point and the others is shown in the graph, take a look.',
                                ' The value is clearly off the limits that define the normal values in the graph.',
                                ],
                         'pt':[ ' Voc?? pode ver pelo gr??fico que a diferen??a entre esse ??ltimo valor e os outros ?? muito alta!',
                                ' A grande discrep??ncia desse valor ?? vis??vel abaixo.',
                                ' Eu achei que seria mais simples mostrar o quanto esse ponto se distancia dos outros na imagem a seguir',
                                ' Visto que essa distor????o ?? enorme, talvez voc?? deva v??-la no gr??fico abaixo.',
                                ' Veja a figura abaixo para que voc?? possa ver a grande diferen??a entre eles.',
                                ' Existe uma grande diferen??a entre esse ponto e os outros, d?? uma olhada.',
                                ' O valor est?? claramente fora dos limites de normalidade pelo gr??fico.',
                                ],
                         }

    outlier_dict_graph2 = {'en':[' You can see the difference between this last value and the others below.',
                                ' Check the graph below to the see this behavior.',
                                ' I believe the image can show this clearly.',
                                ' Take a look in the following data plot.',
                                ' I drew a graph to help you visualize this issue.',
                                ' I made a draft from my analysis, I hope you can see the issue.',
                                ' I considered the situation detailed in the image to determine this is not a normal value.',
                                ' The red point in graph shows the difference between this value and the other ones.',
                                ' It is easy to see the difference from this value and the others below.',
                                ' It is easy to see this situation with the graph.',
                                ' Perhaps it\'s better to see this with the graph below.',
                                ' I think you can see pretty well the data point appearing off the limits in the following picture.',
                                ' The limits considered to be normal are shown in the picture below.',
                                ],
                         'pt':[ ' ?? poss??vel ver a diferen??a entre esse ??ltimo valor e os outros abaixo.',
                                ' Veja esse comportamento no gr??fico abaixo.',
                                ' Eu acredito que a imagem abaixo pode mostrar isso mais claramente.',
                                ' Veja isso na plotagem dos dados seguinte.',
                                ' Eu fiz um gr??fico para ajudar a visualizar isso.',
                                ' Eu fiz um esbo??o da minha an??lise abaixo para ajudar a visualizar essa quest??o.',
                                ' Eu considerei a situa????o detalhada na imagem abaixo para determinar que o valor est?? fora dos padr??es.',
                                ' O ponto vermelho no gr??fico mostra a diferen??a entre esse valor e os outros.',
                                ' ?? f??cil ver a diferen??a entre os valores, d?? uma olhada.',
                                ' ?? simples de ver essa situa????o com um gr??fico.',
                                ' Talvez seja melhor ver isso com o gr??fico abaixo.',
                                ' Eu acho que d?? para ver com clareza como o ??ltimo ponto aparece fora dos limites na figura a seguir.',
                                ' Os limites considerados normais est??o ilustrados na imagem abaixo.',
                                ],
                         }


    outlier_dict_own = {'green':{
                                 'en':[' In short, we had an important improvement.',
                                       ' This is getting better than it was before for sure.',
                                       ' It seems to be a real improvement.',
                                       ' It is important to know what is causing this positive effect.',
                                       ' Let\'s hope we can expand this positive scenario.',
                                       ' I\'m glad there is a good evolution in this KPI.',
                                       ' This is a very good figure.',
                                       ' In general, I think this is a very good sign.',
                                       ' This is definitely a major improvement.'
                                       ],
                                 'pt':[' Resumindo, n??s tivemos uma melhora importante',
                                       ' Isso est?? melhorando em rela????o a per??odos anteriores com toda certeza.',
                                       ' Parece que ?? uma grande melhora de fato.',
                                       ' ?? importante sabermos o que est?? causando esse efeito positivo.',
                                       ' Vamos torcer para que possamos expandir esse cen??rio positivo.',
                                       ' ?? bom sabermos que estamos tendo evolu????o nesse KPI.',
                                       ' ?? uma figura muito boa.',
                                       ' Em geral, acho que ?? um sinal muito bom.',
                                       ' Isso ?? definitivamente uma melhora consider??vel.'
                                       ],
                              },
                         'blue':{
                                 'en':[' This is not necessarily good or bad, but it\'s something we should know.',
                                       ' A change in this kind of KPI is not always positive or negative, but we still should pay attention to it.',
                                       ' This is normally not a critical KPI, we should try to correlate this effect with others.',
                                       ' It is possible that this KPI can affect some others, important to check.',
                                       ' It is possible that it can affect some others KPIs.',
                                       ' This KPI impact isolated is usually not something vital, but this kind of change may point to change on other KPIs.'
                                       ' A major change of this kind can be a sign of a different behavior on other KPIs.',
                                       ' We shouldn\'t neglect this distortion just because it happened on %s %s. This KPI may not be critical, but it usually can be correlated to something bigger.' %(coluna, traffic_type),
                                       ' Although we can\'t define whether this is good or not, we should know what happens.',
                                       ],
                                 'pt':[' Isso n??o ?? necessariamente bom ou ruim, mas ?? algo que devemos saber.',
                                       ' Uma mudan??a nesse KPI n??o ?? sempre positiva ou negativa, mas ainda devemos nos atentar a ela.',
                                       ' Esse n??o ?? normalmente um KPI cr??tico, por??m devemos tentar correlacionar seu efeito com outros indicadores.',
                                       ' ?? poss??vel que esse KPI possa afetar outros, importante verificar essa quest??o.',
                                       ' ?? poss??vel que essa mudan??a afete outros indicadores.',
                                       ' O impacto desse KPI isolado geralmente n??o ?? algo vital, mas esse tipo de mudan??a leva a mudan??as em outros KPIs tamb??m.'
                                       ' Uma mudan??a dessa escala pode ser um sinal de diferen??as em outros KPIs.',
                                       ' N??o devemos negligenciar essa distor????o pelo fato de ter ocorrido em %s %s. Esse indicador pode n??o ser cr??tico, mas normalmente ele pode estar correlacionado a algo maior.' %(coluna, traffic_type),
                                       ' Embora n??o possamos definir se isso ?? bom ou n??o, devemos saber o que acontece.',
                                       ],
                              },
                         'red':{
                                 'en':[' It seems to be problem.',
                                       ' It is important to do something to revert this negative effect.',
                                       ' Let\'s hope we can revert this negative scenario.',
                                       ' I\'m concerned about the evolution of this KPI.',
                                       ' This is really not a good figure.',
                                       ' In general, I think this is not a good sign.',
                                       ],
                                 'pt':[' Parece que ?? um problema.',
                                       ' ?? importante fazer algo para contornar esse efeito negativo.',
                                       ' Esperamos que seja poss??vel reverter esse efeito negativo.',
                                       ' Estou preocupado com a evolu????o desse KPI.',
                                       ' Isso realmente n??o ?? uma boa figura.',
                                       ' Em geral, acho que isso n??o ?? um bom sinal.',
                                       ],
                              },
                         }

    outlier_dict_competitor = {'red':{
                                 'en':[' In short, they had an important improvement.',
                                       ' They are getting better than they were before for sure.',
                                       ' It seems to be a real improvement.',
                                       ' It is important to know what is causing this positive effect.',
                                       ' Let\'s hope we can chase their positive scenario.',
                                       ' This is not a very good figure for us.',
                                       ],
                                 'pt':[' Resumindo, eles tiveram uma melhora importante',
                                       ' Eles est??o melhorando em rela????o a per??odos anteriores com toda certeza.',
                                       ' Parece que ?? uma grande melhora de fato.',
                                       ' ?? importante seguirmos esse cen??rio positivo pelo qual que eles est??o passando tamb??m.',
                                       ' Vamos torcer para que possamos expandir esse cen??rio positivo.',
                                       ' Em geral, acho que n??o ?? um sinal muito bom para n??s.',
                                       ],
                              },
                         'blue':{
                                 'en':[' This is not necessarily good or bad, but it\'s something we should know.',
                                       ' A change in this kind of KPI is not necessarily positive or negative, but we still should pay attention to it.',
                                       ' This is normally not a critical KPI, we should try to correlate this effect with others.',
                                       ' It is possible that this KPI can affect some others, important to check.',
                                       ' It is possible that it can affect some others KPIs.',
                                       ' This KPI impact isolated is usually not something vital, but this kind of change may point to change on other KPIs.'
                                       ' A major change of this kind can be a sign of a different behavior on other KPIs.',
                                       ' We shouldn\'t neglect this distortion just because it happened on %s %s. This KPI may not be critical, but it usually can be correlated to something bigger.' %(coluna, traffic_type),
                                       ' Although we can\'t define whether this is good or not, we should know what happens.',
                                       ],
                                 'pt':[' Isso n??o ?? necessariamente bom ou ruim, mas ?? algo que devemos saber.',
                                       ' Uma mudan??a nesse KPI n??o ?? necessariamente positiva ou negativa, mas ainda devemos nos atentar a ela.',
                                       ' Esse n??o ?? normalmente um KPI cr??tico, por??m devemos tentar correlacionar seu efeito com outros indicadores.',
                                       ' ?? poss??vel que esse KPI possa afetar outros, importante verificar essa quest??o.',
                                       ' ?? poss??vel que essa mudan??a afete outros indicadores.',
                                       ' O impacto desse KPI isolado geralmente n??o ?? algo vital, mas esse tipo de mudan??a leva a mudan??as em outros KPIs tamb??m.'
                                       ' Uma mudan??a dessa escala pode ser um sinal de diferen??as em outros KPIs.',
                                       ' N??o devemos negligenciar essa distor????o pelo fato de ter ocorrido em %s %s. Esse indicador pode n??o ser cr??tico, mas normalmente ele pode estar correlacionado a algo maior.' %(coluna, traffic_type),
                                       ' Embora n??o possamos definir se isso ?? bom ou n??o, devemos saber o que acontece.',
                                       ],
                              },
                         'green':{
                                 'en':[' It seems to be problem for them.',
                                       ' It is important for us to take advantage of this.',
                                       ' Let\'s hope we can grow in their negative moment.',
                                       ' This is really a good figure for us.',
                                       ' In general, I think this is a good sign.',
                                       ],
                                 'pt':[' Parece que ?? um problema para eles.',
                                       ' ?? importante para n??s aproveitarmos esse momento ruim deles.',
                                       ' Esperamos que seja poss??vel crescer nesse momento negativo deles.',
                                       ' Isso realmente ?? uma boa figura para n??s.',
                                       ' Em geral, acho que isso ?? um bom sinal.',
                                       ],
                              },
                         }

    recurrent_dict = {'en':['<br>This is the %s time we are facing this behavior.' %occurences_text[language][last_outs],
                            '<br>This is the %s value I detected with the same behavior.' %occurences_text[language][last_outs],
                            '<br>As you can see, this is not the first time this happens.',
                            '<br>The last %s points are going through this.' %str(last_outs),
                            '<br>This behavior is repeating for a while, it is important to know if everything is fine.',
                            '<br>This is not the first time it happens with this KPI, actually it is the %s time.' %occurences_text[language][last_outs],
                            '<br>Notice this is happening for the %s time.' %occurences_text[language][last_outs],
                            '<br>We have now the last %s occurences in this situation.' %str(last_outs),
                            '<br>The last %s values are outliers with the same behavior.' %str(last_outs),
                            '<br>This is the %s outlier found in this kind of analysis.' %occurences_text[language][last_outs],
                                ],
                     'pt':[ '<br>Essa ?? a %s vez que esse comportamento ocorre.' %occurences_text[language][last_outs],
                            '<br>Os valores tem o mesmo comportamento pela %s vez.' %occurences_text[language][last_outs],
                            '<br>Esse j?? ?? o %s valor encontrado com esse comportamento.' %occurences_text[language][last_outs].replace("a","o"),
                            '<br>Como voc?? pode ver, n??o ?? a primeira vez que isso acontece.',
                            '<br>Os ??ltimos %s pontos est??o passando por isso.' %str(last_outs),
                            '<br>Essa situa????o tem se repetido por algum tempo, talvez seja sentato verificar se est?? tudo certo.',
                            '<br>N??o ?? a primeira vez que isso ocorre com esse KPI, na verdade ?? a %s vez.' %occurences_text[language][last_outs],
                            '<br>Repare que isso j?? aconteceu pela %s vez.' %occurences_text[language][last_outs],
                            '<br>N??s temos agora as ??ltimas %s ocorr??ncias desse jeito.' %str(last_outs),
                            '<br>Os ??ltimos %s valores s??o outliers com mesmo comportamento.' %str(last_outs),
                            '<br>?? o %s outlier encontrado nesse tipo de an??lise.' %occurences_text[language][last_outs].replace("a","o"),
                                ],
                         }

    up_down_dict = {'en':[' This KPI is having big oscilations over time.',
                          ' We can see also there is some up and down outliers.',
                          ' There is a big oscilation in this KPI.',
                          ' The graph shows also a lot of past variations on this.',
                          ' It\'s possible to see other past outliers too, so there is a lot of oscilations on this KPI.',
                          ' We are able to see this KPI\'s behavior goes through a lot of changes.',
                                ],
                     'pt':[ ' Esse KPI est?? tendo muitas oscila????es ao longo do tempo.',
                            ' Podemos ver outliers nas duas dire????es.',
                            ' H?? uma grande oscila????o nesse KPI.',
                            ' O gr??fico tamb??m mostra muitas outras varia????es passadas.',
                            ' ?? poss??vel ver outliers passados tamb??m, onde vemos que existem muitas oscila????es nesse KPI.',
                            ' Podemos ver que o comportamento desse KPI passa por muitas mudan??as.',
                                ],
                         }

    if type_alert[3] == True:
        text = random.choice(outlier_dict1[language][dimension_condition])
    else:
        text = random.choice(outlier_dict2[language][dimension_condition])

    if random.randint(1,100) > 75 and own_condition == 1:
        text += random.choice(outlier_dict_own[color][language])
    elif random.randint(1,100) > 75 and own_condition != 1:
        text += random.choice(outlier_dict_competitor[color][language])

    critical_condition = False   
    if graph == 'yes' and type_alert[3] == True:
        critical_condition = True
    elif graph == 'yes' and type_alert[3] == False:
        critical_condition = False

    if critical_condition == True and random.randint(1,100) > 60 and graph == 'yes':
        text += random.choice(outlier_dict_graph1[language])
    elif random.randint(1,100) > 60 and graph == 'yes':
        text += random.choice(outlier_dict_graph2[language])

    if graph == 'yes' and last_outs > 1:
        recurrent_condition = True
    else:
        recurrent_condition = False

    if recurrent_condition == True and random.randint(1,100) > 10:
        text += random.choice(recurrent_dict[language])

    if graph == 'yes' and (count_pos > 1 and count_neg > 0) or (count_pos > 0 and count_neg > 1):
        up_down_condition = True
    else:
        up_down_condition = False
        
    if up_down_condition == True and random.randint(1,100) > 30:
        text += random.choice(up_down_dict[language])

    return text


def outlier_phrase_zero(coluna, type_alert, traffic_type, current_value, date1, color, sign, format_type, dimension_condition, graph, zero_condition):
    if format_type == int:
        current_value = '{:0,}'.format(current_value)
    elif format_type == float:
        current_value = '{:0,.2f}'.format(current_value)

    #critical situation phrases
    sign_text = {'+':{'green':{
                              'en':['greater','higher','better'],
                              'pt':['maior','mais alto','melhor'],
                              },
                      'red': {
                              'en':['greater','higher','worse'],
                              'pt':['maior','mais alto','pior'],
                              },
                      'blue':{
                              'en':['greater','higher'],
                              'pt':['maior','mais alto'],
                              },
                      },
                 '-':{'green':{'en':['lower','smaller','better'],
                              'pt':['menor','mais baixo','melhor'],
                              },
                      'red': {
                              'en':['lower','smaller','worse'],
                              'pt':['menor','mais baixo','pior'],
                              },
                      'blue':{
                              'en':['lower','smaller'],
                              'pt':['menor','mais baixo'],
                              },
                      }
                 }

    change_word = random.choice(sign_text[sign][color][language])

    #not critical situation phrases
    outlier_dict_zero = {
                'en':{'dimension_on':
                        [
                        '<br><b>%s</b> value for <b>%s</b> was <b>%s</b> on <i>(%s)</i>. The expected value is usually zero, so this is a new kind of detection.<br>'
                        %(coluna, traffic_type, current_value, date1),
                        '<br>The normal value for <b>%s</b> in <b>%s</b> should be zero. We have something different on this KPI for the first time on <i>(%s)</i>, with the value <b>%s</b>.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br>I made a measurement of <b>%s %s</b> for the first time on <i>(%s)</i>, with the value %s. That was unexpected, because all the previous values are null.<br>'
                        %(traffic_type, coluna, date1, current_value),                        
                        '<br>A value of %s was found for <b>%s %s</b> on <i>(%s)</i>. This KPI has always been zero in previous measurements.<br>'
                        %(current_value, traffic_type, coluna, date1),
                        '<br>I found a value out of expectations for <b>%s %s</b> on <i>(%s)</i>. This had never happened before, the values were always zero and now we had <b>%s</b>.<br>'
                        %(traffic_type, coluna, date1, current_value),
                        '<br><b>%s %s</b> was %s on <i>(%s)</i>. Every past value detected was equal to zero, so we are having a new behavior.<br>'
                        %(traffic_type, coluna, current_value, date1),
                        ],
                    'dimension_off':
                        [
                        '<br><b>%s</b> value was <b>%s</b> on <i>(%s)</i>. The expected value is usually zero, so this is a new kind of detection.<br>'
                        %(coluna, current_value, date1),
                        '<br>The normal value for <b>%s</b> should be zero. We have something different on this KPI for the first time on <i>(%s)</i>, with the value <b>%s</b>.<br>'
                        %(coluna, date1, current_value),
                        '<br>I made a measurement of <b>%s</b> for the first time on <i>(%s)</i>, with the value %s. That was unexpected, because all the previous values are null.<br>'
                        %(coluna, date1, current_value),                        
                        '<br>A value of %s was found for <b>%s</b> on <i>(%s)</i>. This KPI has always been zero in previous measurements.<br>'
                        %(current_value, coluna, date1),
                        '<br>I found a value out of expectations for <b>%s</b> on <i>(%s)</i>. This had never happened before, the values were always zero and now we had <b>%s</b>.<br>'
                        %(coluna, date1, current_value),
                        '<br><b>%s</b> was %s on <i>(%s)</i>. Every past value detected was equal to zero, so we are having a new behavior.<br>'
                        %(coluna, current_value, date1),
                        ],
                     },
                'pt':{'dimension_on':
                        [
                        '<br>O valor de <b>%s</b> encontrado para <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>. O valor esperado ?? normalmente zero, ent??o ?? um novo tipo de detec????o.<br>'
                        %(coluna, traffic_type, current_value, date1),
                        '<br>O valor normal de <b>%s</b> em <b>%s</b> deveria ser zero. Temos uma medi????o nesse KPI pela primeira vez no dia <i>(%s)</i>, com valor de <b>%s</b>.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br>Eu fiz uma medi????o em <b>%s</b> em <b>%s</b> pela primeira vez no dia <i>(%s)</i>, com valor de %s. Isso foi inesperado, pois os valores anteriores s??o todos nulos.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br>Foi encontrado um valor de %s para <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Esse KPI sempre foi zero em medi????es anteriores.<br>'
                        %(current_value, coluna, traffic_type, date1),
                        '<br>Encontrei um valor fora do comum para <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Isso nunca havia acontecido antes, o valor era sempre igual a zero e dessa vez foi <b>%s</b>.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br><b>%s</b> em <b>%s</b> apresentou o valor %s no <i>(%s)</i>. Todas as medi????es passadas tinham valor zero, ent??o temos um novo comportamento.<br>'
                        %(coluna, traffic_type, current_value, date1),
                        ],
                     'dimension_off':
                        [
                        '<br>O valor de <b>%s</b> encontrado foi <b>%s</b> no dia <i>(%s)</i>. O valor esperado ?? normalmente zero, ent??o ?? um novo tipo de detec????o.<br>'
                        %(coluna, current_value, date1),
                        '<br>O valor normal de <b>%s</b> deveria ser zero. Temos uma medi????o nesse KPI pela primeira vez no dia <i>(%s)</i>, com valor de <b>%s</b>.<br>'
                        %(coluna, date1, current_value),
                        '<br>Eu fiz uma medi????o em <b>%s</b> pela primeira vez no dia <i>(%s)</i>, com valor de %s. Isso foi inesperado, pois os valores anteriores s??o todos nulos.<br>'
                        %(coluna, date1, current_value),
                        '<br>Foi encontrado um valor de %s em <b>%s</b> no dia <i>(%s)</i>. Esse KPI sempre foi zero em medi????es anteriores.<br>'
                        %(current_value, coluna, date1),
                        '<br>Encontrei um valor fora do comum para <b>%s</b> no dia <i>(%s)</i>. Isso nunca havia acontecido antes, o valor era sempre igual a zero e dessa vez foi <b>%s</b>.<br>'
                        %(coluna, date1, current_value),
                        '<br><b>%s</b> apresentou o valor %s no <i>(%s)</i>. Todas as medi????es passadas tinham valor zero, ent??o temos um novo comportamento.<br>'
                        %(coluna, current_value, date1),
                        ],
                     }
                }

    outlier_dict_cl_zero = {
                'en':{'dimension_on':
                        [
                        '<br><b>%s</b> value for <b>%s</b> was <b>%s</b> on <i>(%s)</i>. The expected value is usually near zero, so this is a new kind of detection.<br>'
                        %(coluna, traffic_type, current_value, date1),
                        '<br>The normal value for <b>%s</b> in <b>%s</b> should be around zero. We have something different on this KPI on <i>(%s)</i>, with the value %s.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br>I made a significant measurement of <b>%s %s</b> on <i>(%s)</i>, with the value %s. That was unexpected, because all the previous values are almost null.<br>'
                        %(traffic_type, coluna, date1, current_value),                        
                        '<br>A value of %s was found for <b>%s %s</b> on <i>(%s)</i>. This KPI has always been very close to zero in previous measurements.<br>'
                        %(current_value, traffic_type, coluna, date1),
                        '<br>I found a value out of expectations for <b>%s %s</b> on <i>(%s)</i>. This happens very rarely, the values were always near zero and now we had %s.<br>'
                        %(traffic_type, coluna, date1, current_value),
                        '<br><b>%s %s</b> was %s on <i>(%s)</i>. Every past value detected was close or equal to zero, so we are having a new behavior.<br>'
                        %(traffic_type, coluna, current_value, date1),
                        ],
                    'dimension_off':
                        [
                        '<br><b>%s</b> value was <b>%s</b> on <i>(%s)</i>. The expected value is usually near zero, so this is a new kind of detection.<br>'
                        %(coluna, current_value, date1),
                        '<br>The normal value for <b>%s</b> should be around zero. We have something different on this KPI on <i>(%s)</i>, with the value %s.<br>'
                        %(coluna, date1, current_value),
                        '<br>I made a significant measurement of <b>%s</b> on <i>(%s)</i>, with the value %s. That was unexpected, because all the previous values are almost null.<br>'
                        %(coluna, date1, current_value),                        
                        '<br>A value of %s was found for <b>%s</b> on <i>(%s)</i>. This KPI has always been very close to zero in previous measurements.<br>'
                        %(current_value, coluna, date1),
                        '<br>I found a value out of expectations for <b>%s</b> on <i>(%s)</i>. This happens very rarely, the values were always near zero and now we had %s.<br>'
                        %(coluna, date1, current_value),
                        '<br><b>%s</b> was %s on <i>(%s)</i>. Every past value detected was close or equal to zero, so we are having a new behavior.<br>'
                        %(coluna, current_value, date1),
                        ],
                     },
                'pt':{'dimension_on':
                        [
                        '<br>O valor de <b>%s</b> encontrado para <b>%s</b> foi <b>%s</b> no dia <i>(%s)</i>. O valor esperado ?? normalmente perto de zero, ent??o ?? um novo tipo de detec????o.<br>'
                        %(coluna, traffic_type, current_value, date1),
                        '<br>O valor normal de <b>%s</b> em <b>%s</b> deveria ser por volta de zero. Temos uma medi????o diferente nesse KPI no dia <i>(%s)</i>, com valor de %s.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br>Eu fiz uma medi????o significante em <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>, com valor de %s. Isso foi inesperado, pois os valores anteriores s??o quase todos nulos.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br>Foi encontrado um valor de %s para <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Esse KPI sempre foi muito pr??ximo de zero em medi????es anteriores.<br>'
                        %(current_value, coluna, traffic_type, date1),
                        '<br>Encontrei um valor fora do comum para <b>%s</b> em <b>%s</b> no dia <i>(%s)</i>. Isso praticamente nunca havia acontecido antes, o valor era sempre perto de zero e dessa vez foi %s.<br>'
                        %(coluna, traffic_type, date1, current_value),
                        '<br><b>%s</b> em <b>%s</b> apresentou o valor %s no <i>(%s)</i>. Todas as medi????es passadas tinham valor perto ou igual zero, ent??o temos um novo comportamento.<br>'
                        %(coluna, traffic_type, current_value, date1),
                        ],
                     'dimension_off':
                        [
                        '<br>O valor de <b>%s</b> encontrado foi <b>%s</b> no dia <i>(%s)</i>. O valor esperado ?? normalmente perto de zero, ent??o ?? um novo tipo de detec????o.<br>'
                        %(coluna, current_value, date1),
                        '<br>O valor normal de <b>%s</b> deveria ser por volta de zero. Temos uma medi????o nesse KPI no dia <i>(%s)</i>, com valor de %s.<br>'
                        %(coluna, date1, current_value),
                        '<br>Eu fiz uma medi????o significante em <b>%s</b> no dia <i>(%s)</i>, com valor de %s. Isso foi inesperado, pois os valores anteriores s??o quase todos nulos.<br>'
                        %(coluna, date1, current_value),
                        '<br>Foi encontrado um valor de %s em <b>%s</b> no dia <i>(%s)</i>. Esse KPI sempre foi muito pr??ximo de zero em medi????es anteriores.<br>'
                        %(current_value, coluna, date1),
                        '<br>Encontrei um valor fora do comum para <b>%s</b> no dia <i>(%s)</i>. Isso praticamente nunca havia acontecido antes, o valor era sempre perto de zero e dessa vez foi %s.<br>'
                        %(coluna, date1, current_value),
                        '<br><b>%s</b> apresentou o valor %s no <i>(%s)</i>. Todas as medi????es passadas tinham valor perto ou igual zero, ent??o temos um novo comportamento.<br>'
                        %(coluna, current_value, date1),
                        ],
                     }
                }


    if zero_condition == 'zero':
        text = random.choice(outlier_dict_zero[language][dimension_condition])
    elif zero_condition == 'close_to_zero':
        text = random.choice(outlier_dict_cl_zero[language][dimension_condition])

    return text



# --------------------------------------------- TRENDS PART ---------------------------------------------------------

def trend_phrase(traffic_type, coluna, type_alert, color, trend_type, format_type, dimension_condition):

    trend_dict = {
                'en':{
                     'falling':'falling',
                     'rising':'rising',
                     'linear falling':'falling',
                     'linear rising':'rising',
                     'exponencial falling':'exponencial',
                     'exponencial rising':'exponencial',
                     'logarithmic falling':'logarithmic',
                     'logarithmic rising':'logarithmic',
                      },
                'pt':{
                     'falling':'de queda',
                     'rising':'de crescimento',
                     'linear falling':'linear de queda',
                     'linear rising':'linear de crescimento',
                     'exponencial falling':'exponencial de queda',
                     'exponencial rising':'exponencial de crescimento',
                     'logarithmic falling':'logar??tmica de queda',
                     'logarithmic rising':'logar??tmica de crescimento',
                      },
                }

    trend_type = trend_dict[language][trend_type]
    #critical situation phrases
    trends_dict1 = {'dimension_on':{
                        'en':[
                            '<br>There is a <span style="color:%s"><b>strong %s</b></span> trend in <b>%s %s</b>.' %(color, trend_type, traffic_type, coluna),
                            '<br><b>%s %s</b> is in a very high <span style="color:%s"><b> %s</b></span> trend.' %(traffic_type, coluna, color, trend_type),
                            '<br><b>%s %s</b> is facing a <span style="color:%s"><b>solid %s</b></span> trend.' %(traffic_type, coluna, color, trend_type),
                            '<br>There seems to be a <span style="color:%s"><b>%s</b></span> trend in <b>%s %s</b>.' %(color, trend_type, traffic_type, coluna),
                            '<br>I found out that <b>%s %s</b> is showing a <span style="color:%s"><b>strong %s</b></span> trend.' %(traffic_type, coluna, color, trend_type),
                            '<br>I\'ve noticed a strong correlation in a <span style="color:%s"><b>%s</b></span> trend in <b>%s %s</b>.' %(color, trend_type, traffic_type, coluna),
                            '<br>There is an incredibly strong correlation in a <span style="color:%s"><b>%s</b></span> trend detected in <b>%s %s</b>. It\'s more than 0.99 of correlation!' %(color, trend_type, traffic_type, coluna),
                            ],
                        'pt':
                            [
                            '<br>Existe uma forte tend??ncia <span style="color:%s"><b>%s</b></span> encontrada em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Foi encontrada uma forte tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Percebi um movimento que indica tend??ncia consider??vel <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Os ??ltimos valores mostram um movimento significativo <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Parece que existe uma tend??ncia de grande correla????o <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Existe uma correla????o forte em uma tend??ncia <span style="color:%s"><b>%s</b></span> encontrada em <b>%s</b> em <b>%s</b>. ?? de mais de 0.99!' %(color, trend_type, traffic_type, coluna),
                            ]
                        },
                    'dimension_off':{
                        'en':[
                            '<br>There is a <span style="color:%s"><b>strong %s</b></span> trend in <b>%s</b>.' %(color, trend_type, coluna),
                            '<br><b>%s</b> is in a very high <span style="color:%s"><b>%s</b></span> trend.' %(coluna, color, trend_type),
                            '<br><b>%s</b> is facing a <span style="color:%s"><b>solid %s</b></span> trend.' %(coluna, color, trend_type),
                            '<br>There seems to be a <span style="color:%s"><b>%s</b></span> trend in <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>I found out that <b>%s</b> is showing a <span style="color:%s"><b>strong %s</b></span> trend.' %(coluna, color, trend_type),
                            '<br>I\'ve noticed a strong correlation in a <span style="color:%s"><b>%s</b></span> trend in <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>There is an incredibly strong correlation in a <span style="color:%s"><b>%s</b></span> trend detected in <b>%s</b>. It\'s more than 0.99 of correlation!' %(color, trend_type, coluna),
                            ],
                        'pt':
                            [
                            '<br>Existe uma forte tend??ncia <span style="color:%s"><b>%s</b></span> encontrada em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Foi encontrada uma forte tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Percebi um movimento que indica tend??ncia consider??vel <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Os ??ltimos valores mostram um movimento significativo <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Parece que existe uma tend??ncia de grande correla????o <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Existe uma correla????o forte em uma tend??ncia <span style="color:%s"><b>%s</b></span> encontrada em <b>%s</b>. ?? de mais de 0.99!' %(color, trend_type, coluna),
                            ]
                        }
                    }
    
    #not critical situation phrases
    trends_dict2 = {'dimension_on':{
                        'en':[
                            '<br>There is a <span style="color:%s"><b>%s</b></span> trend in <b>%s %s</b>.' %(color, trend_type, traffic_type, coluna),
                            '<br><b>%s %s</b> is in a <span style="color:%s"><b>%s</b></span> trend.' %(traffic_type, coluna, color, trend_type),
                            '<br><b>%s %s</b> is facing a <span style="color:%s"><b>%s</b></span> trend.' %(traffic_type, coluna, color, trend_type),
                            '<br>There seems to be a <span style="color:%s"><b>%s</b></span> trend in <b>%s %s</b>.' %(color, trend_type, traffic_type, coluna),
                            '<br>I noticed a <span style="color:%s"><b>%s</b></span> trend in <b>%s %s</b>.' %(color, trend_type, traffic_type, coluna),
                            '<br>I found out that <b>%s %s</b> is showing a <span style="color:%s"><b>%s</b></span> trend.' %(traffic_type, coluna, color, trend_type),
                            '<br><b>%s %s</b> values are going through a <span style="color:%s"><b>%s</b></span> trend moviment.' %(traffic_type, coluna, color, trend_type),
                            '<br>I\'ve noticed a correlation in a <span style="color:%s"><b>%s</b></span> trend in <b>%s %s</b>.' %(color, trend_type, traffic_type, coluna),
                            ],
                        'pt':
                            [
                            '<br>Existe uma tend??ncia <span style="color:%s"><b>%s</b></span> encontrada em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Foi encontrada uma tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Percebi um movimento que indica tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Os ??ltimos valores mostram um movimento <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                            '<br>Parece que existe uma tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b> em <b>%s</b>.' %(color, trend_type, coluna, traffic_type),
                             ],
                        },
                    'dimension_off':{
                        'en':[
                            '<br>There is a <span style="color:%s"><b>%s</b></span> trend in <b>%s</b>.' %(color, trend_type, coluna),
                            '<br><b>%s</b> is in a <span style="color:%s"><b>%s</b></span> trend.' %(coluna, color, trend_type),
                            '<br><b>%s</b> is facing a <span style="color:%s"><b>%s</b></span> trend.' %(coluna, color, trend_type),
                            '<br>There seems to be a <span style="color:%s"><b>%s</b></span> trend in <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>I noticed a <span style="color:%s"><b>%s</b></span> trend in <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>I found out that <b>%s</b> is showing a <span style="color:%s"><b>%s</b></span> trend.' %(coluna, color, trend_type),
                            '<br><b>%s</b> values are going through a <span style="color:%s"><b>%s</b></span> trend moviment.' %(coluna, color, trend_type),
                            '<br>I\'ve noticed a correlation in a <span style="color:%s"><b>%s</b></span> trend in <b>%s</b>.' %(color, trend_type, coluna),
                            ],
                        'pt':
                            [
                            '<br>Existe uma tend??ncia <span style="color:%s"><b>%s</b></span> encontrada em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Foi encontrada uma tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Percebi um movimento que indica tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Os ??ltimos valores mostram um movimento <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                            '<br>Parece que existe uma tend??ncia <span style="color:%s"><b>%s</b></span> em <b>%s</b>.' %(color, trend_type, coluna),
                             ],
                        }
                    }

    trend_dict_graph = {'en':[  ' You can see the trend behavior below.',
                                ' The correlation is shown in the following image.',
                                ' Take a look in the evolution of the values over time.',
                                ' I thought it would be easier to how much the values are connected with the graphic',
                                ' I made a graph of the correlation, take a look.',
                                ],
                         'pt':[ ' Voc?? pode ver o comportamento dessa tend??ncia abaixo.',
                                ' A correla????o est?? mostrada na figura seguinte.',
                                ' Veja a evolu????o dos valores ao longo do tempo.',
                                ' Eu achei que seria mais f??cil mostrar a conex??o entre os valores com o gr??fico',
                                ' Eu fiz um gr??fico da correla????o, veja abaixo.',
                                ],
                         }

    trend_dict_own = {'green':{
                                 'en':[' Let\'s hope the values keep going on this trend.',
                                       ' This is a good sign for the website.',
                                       ' This means we have a positive scenario.',
                                       ' In general, I can say the website is doing well for this.',
                                       ],
                                 'pt':[' Vamos torcer para que os valores sigam nessa tend??ncia.',
                                       ' Isso ?? um bom sinal para o site.',
                                       ' Isso significa que temos um cen??rio positivo.',
                                       ' Em geral, posso dizer que o site est?? indo bem nisso.',
                                       ],
                              },
                         'blue':{
                                 'en':[' This is not necessarily good or bad, but it\'s something we should know.',
                                       ' Although we can\'t define whether this is good or not, we should know what happens.',
                                       ],
                                 'pt':[' Isso n??o ?? necessariamente bom ou ruim, mas ?? algo que devemos saber.',
                                       ' Embora n??o possamos definir se isso ?? bom ou n??o, devemos saber o que acontece.',
                                       ],
                              },
                         'red':{
                                 'en':[' Let\'s hope we can reverse this kind of trend.',
                                       ' This is not a good sign for the website.',
                                       ' This means we don\'t have a very positive scenario.',
                                       ' In general, I can say the website has some problems with this.',
                                       ],
                                 'pt':[' Vamos torcer para que possamos reverter tend??ncia.',
                                       ' Isso n??o ?? um bom sinal para o site.',
                                       ' Isso significa que n??o temos um cen??rio muito bom.',
                                       ' Em geral, posso dizer que o site est?? tendo alguns problemas com nisso.',
                                       ],
                              },
                         }

    trend_dict_competitor = {'red':{
                                 'en':[' Let\'s hope we can follow their trend.',
                                       ' This is a good sign for their website.',
                                       ' This means they have a positive scenario.',
                                       ' In general, I can say their website is doing well for this.',
                                       ],
                                 'pt':[' Vamos torcer para que possamos seguir essa tend??ncia tamb??m.',
                                       ' Isso ?? um bom sinal para o site deles.',
                                       ' Isso significa que eles tem um cen??rio positivo.',
                                       ' Em geral, posso dizer que o site deles est?? indo bem nisso.',
                                       ],
                              },
                         'blue':{
                                 'en':[' This is not necessarily good or bad, but it\'s something we should know.',
                                       ' Although we can\'t define whether this is good or not, we should know what happens.',
                                       ],
                                 'pt':[' Isso n??o ?? necessariamente bom ou ruim, mas ?? algo que devemos saber.',
                                       ' Embora n??o possamos definir se isso ?? bom ou n??o, devemos saber o que acontece.',
                                       ],
                              },
                         'green':{
                                 'en':[' Their trend in unfavorable, it\'s a good moment to take advantage of it',
                                       ' This is not a good sign for their website.',
                                       ' This means they don\'t have a very positive scenario.',
                                       ' In general, I can say their website has some problems with this.',
                                       ],
                                 'pt':[' A tend??cia deles ?? desfavor??vel, ?? um momento para ser aproveitado.',
                                       ' Isso n??o ?? um bom sinal para o site deles.',
                                       ' Isso significa que eles n??o est??o em um cen??rio muito bom.',
                                       ' Em geral, posso dizer que o site deles est?? tendo alguns problemas com nisso.',
                                       ],
                              },
                         }
    
    if type_alert[3] == True:
        trend = random.choice(trends_dict1[dimension_condition][language])
    else:
        trend = random.choice(trends_dict2[dimension_condition][language])

    if random.randint(1,100) > 20 and own_condition == 1:
        trend += random.choice(trend_dict_own[color][language])
    elif random.randint(1,100) > 20 and own_condition != 1:
        trend += random.choice(trend_dict_competitor[color][language])

    if random.randint(1,100) > 70:
        trend += random.choice(trend_dict_graph[language])
    return trend


# --------------------------------------------- EMAIL SECTION TITLES PART -----------------------------------------------------

def title_to_email_section(main_topic, alert_type):
    title_dict1 = {
        'en':[
              '%s KPIs analysis show significant values distortion' %main_topic,
              '%s KPIs analysis seem to present unusual values' %main_topic,
              '%s analysis points to unexpected values presence' %main_topic,
              '%s seem to have unusual values' %main_topic,
            ],
        'pt':
            ['A an??lise de KPIs de %s indica algumas distor????es de valores significantes' %main_topic,
              'A an??lise de KPIs de %s apresentou alguns valores inesperados' %main_topic,
              '%s t??m mostrado a presen??a tem valores inesperados' %main_topic,
              '%s aparentemente est?? com alguns valores fora do normal' %main_topic,
            ]
        }

    title_dict2 = {
        'en':[
            '%s had changes compared to their last performed test' %main_topic,
            '%s had changes compared to their last Simplex test' %main_topic,
            '%s seems to show different values' %main_topic,
            '%s has faced some changes' %main_topic,
            ],
        'pt':
            ['O %s indica algumas mudan??as em rela????o ao ??ltimo valor medido' %main_topic,
             'A an??lise feita em %s apresentou algumas mudan??as' %main_topic,
             '%s apresenta diferen??a em rela????o aos ??ltimos valores capturados' %main_topic,
             '%s apresenta mudan??a em rela????o ??s ??ltimas medi????es' %main_topic,
            ]
        }

    title_dict3 = {
        'en':[
            '%s Report' %main_topic,
            ],
        'pt':
            ['Relat??rio de %s' %main_topic,
            ]
        }

    if alert_type == 'unusual':
        title = '<div style="color:white;font-size:18px;background-color:black;text-align:left;padding-left:20px"><br>' + random.choice(title_dict1[language]) + '<br><br></div>'
    elif alert_type == 'change':
        title = '<div style="color:white;font-size:18px;background-color:black;text-align:left;padding-left:20px"><br>' + random.choice(title_dict2[language]) + '<br><br></div>'        
    elif alert_type == 'report':
        title = '<div style="color:white;font-size:18px;background-color:black;text-align:left;padding-left:20px"><br>' + random.choice(title_dict3[language]) + '<br><br></div>'        
    return title

# ----------------------------------------- GRAPHICS INFORMATION PART -----------------------------------------------

def get_graph_values(domain, variable, var_type, dates, analysis, weekday, graphic_type):
    graph_title_period_dict = {'weekdays':{
                                'en': ['Mondays','Tuesdays','Wednesdays','Thursdays','Fridays','Saturdays','Sundays'],
                                'pt': ['Segundas','Ter??as','Quartas','Quintas','Sextas','S??bados','Domingos'],
                                },
                        'days':{
                                'en': 'in the last %s days' %len(dates),
                                'pt': 'nos ??ltimos %s dias' %len(dates),
                                },
                        'hours':{
                                'en': 'in the last %s hours' %len(dates),
                                'pt': 'nas ??ltimas %s horas' %len(dates),
                                },
                        'weeks':{
                                'en': 'in the last 10 entire weeks',
                                'pt': 'nas ??ltimas 10 semanas inteiras',
                                }
                        }

    if analysis == 'weekdays':
        analysisperiod = graph_title_period_dict[analysis][language][weekday]
        if language == 'en':
            analysisperiod = "in the last " + analysisperiod
        elif language == 'pt' and analysisperiod in ['Segundas','Ter??as','Quartas','Quintas','Sextas']:
            analysisperiod = "nas ??ltimas " + analysisperiod
        elif language == 'pt':
            analysisperiod = "nos ??ltimos " + analysisperiod
        
    elif analysis == 'days' or analysis == 'hours' or analysis == 'weeks':
        analysisperiod = graph_title_period_dict[analysis][language]

    if var_type != '':
        if language in ['en']:
            variable = var_type + " " + variable
        elif language in ['pt']:
            variable = variable + " em " + var_type

    graph_title_dict = {'outlier':
                             {
                           'en':'%s %s' %(variable, analysisperiod),
                           'pt':'%s %s' %(variable, analysisperiod),
                           },
                        'trend':
                             {
                           'en':'%s Trend %s' %(variable, analysisperiod),
                           'pt':'Tend??ncia de %s %s' %(variable, analysisperiod),
                           },
                        'performance':
                             {
                           'en':'Criteria with Greatest Negative Impact Which Still Needs Improvement',
                           'pt':'Criterios com Maior Impacto Negativo que Ainda Precisam de Ajustes',
                           },
                        'security':
                             {
                           'en':'Criteria with Greatest Negative Impact in Score',
                           'pt':'Criterios com Maior Impacto Negativo na Nota',
                           },
                        'Top 5':
                             {
                           'en':'Top 5 %s %s' %(variable, analysisperiod),
                           'pt':'Top 5 %s %s' %(variable, analysisperiod),
                           },
                         
                        }
    
    graph_text_dict = {'outlier':{
                            'en':{'expected':'Expected value',
                                  'upper_limit':'Upper Limit',
                                  'lower_limit':'Lower Limit',
                                  },
                            'pt':{'expected':'Valor esperado',
                                  'upper_limit':'Limite superior',
                                  'lower_limit':'Limite inferior',
                                  },
                          }
                   }

    graph_title = graph_title_dict[graphic_type][language]        
    if graphic_type == 'outlier':
        expected_value = graph_text_dict[graphic_type][language]['expected']
        upper_limit = graph_text_dict[graphic_type][language]['upper_limit']
        lower_limit = graph_text_dict[graphic_type][language]['lower_limit']
        return graph_title, expected_value, upper_limit, lower_limit

    elif graphic_type in ['trend','performance','security','Top 5']:
        return graph_title


# ------------------------------------------- VALUES COMPARISON ---------------------------------------------
def get_comparison_phrases(siteurl, traffic_type, value0, date0, value1, date1, sign, color, varpercdelta, type_alert, format_type, numbers):
    if format_type == int:
        value0 = '{:0,}'.format(value0)
        value1 = '{:0,}'.format(value1)
    elif format_type == float:
        value0 = '{:0,.2f}'.format(value0)
        value1 = '{:0,.2f}'.format(value1)    
    

    sign_text = {'+':{'green':{
                            'en':[{'singular':['has grown','has raised'],'plural':['have grown','have raised']},['increase','growth','improvement']],
                            'pt':[{'singular':['cresceu','subiu','aumentou'],'plural':['cresceram','subiram']},['ganho','aumento','crescimento','melhora']],
                              },
                      'red':{
                            'en':[{'singular':['has grown','has raised'],'plural':['have grown','have raised']},['increase','growth']],
                            'pt':[{'singular':['cresceu','subiu','aumentou'],'plural':['cresceram','subiram']},['perda','aumento','crescimento','piora']],
                               },
                      'blue':{
                            'en':[{'singular':['has grown','has raised'],'plural':['have grown','have raised']},['change','increase','growth']],
                            'pt':[{'singular':['cresceu','subiu','aumentou'],'plural':['cresceram','subiram']},['aumento','crescimento','mudan??a']],
                            },
                      },               
                 '-':{'green':{
                            'en':[{'singular':['has dropped','has fallen'],'plural':['have dropped','have fallen']},['decrease','drop','improvement']],
                            'pt':[{'singular':['caiu','diminuiu'],'plural':['ca??ram','diminu??ram']},['diminui????o','melhora']],
                             },
                      'red':{
                            'en':[{'singular':['has dropped','has fallen'],'plural':['have dropped','have fallen']},['decrease','drop']],
                            'pt':[{'singular':['caiu','diminuiu'],'plural':['ca??ram','diminu??ram']},['perda','queda','retra????o']],
                            },
                      'blue':{
                            'en':[{'singular':['has dropped','has fallen'],'plural':['have dropped','have fallen']},['change','decrease','drop']],
                            'pt':[{'singular':['caiu','diminuiu'],'plural':['ca??ram','diminu??ram']},['diminui????o','mudan??a']],
                            },
                      },
                }

    change_word1 = random.choice(sign_text[sign][color][language][0][numbers])        
    change_word2 = random.choice(sign_text[sign][color][language][1])

    #critical situation phrases
    comparison_dict1 = {
                'en':[
                    '<br><b><a href="%s">%s</a> %s</b> %s from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. <b><span style="color:%s;">%s</span></b> of %s is a very high value change.<br>' \
                    %(siteurl, siteurl, traffic_type, change_word1, value0, date0, value1, date1, color, '{:.2%}'.format(varpercdelta), change_word2),
                    '<br><b><a href="%s">%s</a> %s</b> %s from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. This represents a very high value change of %s, which is <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(siteurl, siteurl, traffic_type, change_word1, value0, date0, value1, date1, change_word2, color, '{:.2%}'.format(varpercdelta)),
                    '<br>There is a very big %s in <b><a href="%s">%s</a> %s</b> from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. %s of <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(change_word2, siteurl, siteurl, traffic_type, value0, date0, value1, date1, random.choice(sign_text[sign][color][language][1]).title(), color, '{:.2%}'.format(varpercdelta)),
                    '<br>There is a considerable %s from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i> detected in <b><a href="%s">%s</a> %s</b>. This means <b><span style="color:%s;">%s</span></b> of %s, so it\'s a critical change.<br>' \
                    %(change_word2, value0, date0, value1, date1, siteurl, siteurl, traffic_type, color, '{:.2%}'.format(varpercdelta), random.choice(sign_text[sign][color][language][1])),
                    '<br>I see a critical change in <b>%s</b>. It\'s value for <b><a href="%s">%s</a></b> %s from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. This represents <b><span style="color:%s;">%s</span></b> of %s.<br>' \
                    %(traffic_type, siteurl, siteurl, change_word1, value0, date0, value1, date1 , color, '{:.2%}'.format(varpercdelta), change_word2),
                    ],
                'pt':
                    [
                    '<br><b>%s</b> de <b><a href="%s">%s</a></b> %s de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. Visto que temos <b><span style="color:%s;">%s</span></b> de %s, ?? uma grande mudan??a.<br>' \
                    %(traffic_type.title(), siteurl, siteurl, change_word1, value0, date0, value1, date1, color, '{:.2%}'.format(varpercdelta), change_word2),
                    '<br><b>%s</b> de <b><a href="%s">%s</a></b> %s de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. Isso representa grande %s, no valor de <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(traffic_type.title(), siteurl, siteurl, change_word1, value0, date0, value1, date1, change_word2, color, '{:.2%}'.format(varpercdelta)),
                    '<br>Existe %s muito grande no <b>%s</b> de <b><a href="%s">%s</a></b>, pois ele foi de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. %s de <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(change_word2, traffic_type, siteurl, siteurl, value0, date0, value1, date1, random.choice(sign_text[sign][color][language][1]).title(), color, '{:.2%}'.format(varpercdelta)),
                    '<br>H?? %s consider??vel de <b>%s</b>, pois houve uma mudan??a detectada de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i> em <b><a href="%s">%s</a></b>. Isso indica <b><span style="color:%s;">%s</span></b> de %s, ent??o ?? uma mudan??a cr??tica.<br>' \
                    %(change_word2, traffic_type, value0, date0, value1, date1, siteurl, siteurl, color, '{:.2%}'.format(varpercdelta), random.choice(sign_text[sign][color][language][1])),
                    '<br>Eu vejo uma mudan??a cr??tica em <b>%s</b>. Seu valor em <b><a href="%s">%s</a></b> %s de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. Isso representa <b><span style="color:%s;">%s</span></b> de %s.<br>' \
                    %(traffic_type, siteurl, siteurl, change_word1, value0, date0, value1, date1 , color, '{:.2%}'.format(varpercdelta), change_word2),
                     ],
                }

    #not critical situation phrases
    comparison_dict2 = {
                'en':[
                    '<br><b><a href="%s">%s</a> %s</b> %s from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. %s of <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(siteurl, siteurl, traffic_type, change_word1, value0, date0, value1, date1, change_word2.title(), color, '{:.2%}'.format(varpercdelta)),
                    '<br>There is a %s in <b><a href="%s">%s</a> %s</b> from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. %s of <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(change_word2, siteurl, siteurl, traffic_type, value0, date0, value1, date1, random.choice(sign_text[sign][color][language][1]).title(), color, '{:.2%}'.format(varpercdelta)),
                    '<br>There is a %s from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i> detected in <b><a href="%s">%s</a> %s</b>. This means <b><span style="color:%s;">%s</span></b> of %s.<br>' \
                    %(change_word2, value0, date0, value1, date1, siteurl, siteurl, traffic_type, color, '{:.2%}'.format(varpercdelta), random.choice(sign_text[sign][color][language][1])),
                    '<br>The <b>%s</b> value for <b><a href="%s">%s</a></b> %s from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. This represents <b><span style="color:%s;">%s</span></b> of %s.<br>' \
                    %(traffic_type, siteurl, siteurl, change_word1, value0, date0, value1, date1 , color, '{:.2%}'.format(varpercdelta), change_word2),
                    ],
                'pt':
                    [
                    '<br><b>%s</b> de <b><a href="%s">%s</a></b> %s de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. Isso representa %s de <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(traffic_type.title(), siteurl, siteurl, change_word1, value0, date0, value1, date1, change_word2, color, '{:.2%}'.format(varpercdelta)),
                    '<br>Existe %s no <b>%s</b> de <b><a href="%s">%s</a></b>, pois ele saiu de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. %s de <b><span style="color:%s;">%s</span></b>.<br>' \
                    %(change_word2, traffic_type, siteurl, siteurl, value0, date0, value1, date1, random.choice(sign_text[sign][color][language][1]).title(), color, '{:.2%}'.format(varpercdelta)),
                    '<br>H?? %s de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i> detectado no <b>%s</b> de <b><a href="%s">%s</a></b>. Isso indica <b><span style="color:%s;">%s</span></b> de %s.<br>' \
                    %(change_word2, value0, date0, value1, date1, traffic_type, siteurl, siteurl, color, '{:.2%}'.format(varpercdelta), random.choice(sign_text[sign][color][language][1])),
                    '<br>O valor de <b>%s</b> em <b><a href="%s">%s</a></b> %s de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. Isso representa <b><span style="color:%s;">%s</span></b> de %s.<br>' \
                    %(traffic_type, siteurl, siteurl, change_word1, value0, date0, value1, date1 , color, '{:.2%}'.format(varpercdelta), change_word2),
                     ],
                }

    if type_alert[3] == True:
        comparison_phrase = random.choice(comparison_dict1[language])
    else:
        comparison_phrase = random.choice(comparison_dict2[language])
    return comparison_phrase

def get_comparison_phrases_zero(siteurl, traffic_type, date0, value1, date1, color, format_type):
    if format_type == int:
        value1 = '{:0,}'.format(value1)
    elif format_type == float:
        value1 = '{:0,.2f}'.format(value1)    
    
    comparison_dict = {
                    'en':['<br><b>%s</b> value for <b><a href="%s">%s</a></b> was <span style="color:%s;"><b>%s</b></span> on <i>(%s)</i>. The previous value was zero on <i>(%s)</i>.<br>'
                        %(traffic_type.title(), siteurl, siteurl, color, value1, date1, date0),
                        '<br>The last value for <b>%s</b> in <b><a href="%s">%s</a></b> was zero. We have something different on this KPI on <i>(%s)</i>, with the value <span style="color:%s;"><b>%s</b></span>.<br>'
                        %(traffic_type, siteurl, siteurl, date1, color, value1),
                        '<br>I made a measurement of <b>%s <a href="%s">%s</a></b> on <i>(%s)</i>, with the value <span style="color:%s;"><b>%s</b></span>. This means the value is not zero anylonger as it was on <i>(%s)</i>.<br>'
                        %(traffic_type, siteurl, siteurl, date1, color, value1, date0),                        
                        ],

                    'pt':['<br>O valor de <b>%s</b> encontrado para <b><a href="%s">%s</a></b> foi <span style="color:%s;"><b>%s</b></span> no dia <i>(%s)</i>. O valor anterior era zero no dia <i>(%s)</i>.<br>'
                        %(traffic_type, siteurl, siteurl, color, value1, date1, date0),
                        '<br>O ??ltimo valor de <b>%s</b> em <b><a href="%s">%s</a></b> foi zero no dia <i>(%s)</i>. Agora temos uma medi????o com valor de <span style="color:%s;"><b>%s</b></span> no dia <i>(%s)</i>.<br>'
                        %(traffic_type, siteurl, siteurl, date0, color, value1, date1),
                        '<br>Eu fiz uma medi????o de <b>%s</b> em <b><a href="%s">%s</a></b> no dia <i>(%s)</i> com valor de <span style="color:%s;"><b>%s</b></span>. Isso mostra grande mudan??a de valor, pois ele era zero em <i>(%s)</i>.<br>'
                        %(traffic_type, siteurl, siteurl, date1, color, value1, date0),
                        ],
                }

    comparison_phrase = random.choice(comparison_dict[language])
    return comparison_phrase

def fill_up_similar_comment(number_addtext , number_urltext, type_check):
    #comment after agregating alerts (outlier or trend)
    if type_check == 'outlier':
        topic = {'en':'outliers',
                 'pt':'outliers',
                 }
    elif type_check == 'trends':
        topic = {'en':'trends',
                 'pt':'tend??ncias',
                 }        
    topic = topic[language]

    fill_up_dict = {'en':['I have more considerations about this %s topic.<br>' %topic,
                          'You should also know that ',
                          'Just to let you know, ',
                          'Just in case, please know that ',
                          'Let me tell you also that ',
                          'Just to finish this topic, ',
                          'There are still some issues about this.<br>',
                          ],
                    'pt':['Eu tenho mais uma considera????o sobre esse t??pico de %s.<br>' %topic,
                          'Voc?? deveria saber tamb??m que ',
                          'Apenas avisando, ',
                          'Eu queria ressaltar tamb??m que ',
                          'Finalizando esse t??pico, ',
                          'Ainda existem algumas quest??es em rela????o a isso.<br>',
                          ],
                    }

    comment_phrase = ''
    if random.randint(1,100) > 10 and number_urltext > 0 and number_addtext == 0:
        comment_phrase += random.choice(fill_up_dict[language])

    return comment_phrase

'''
def get_all_elements_as_text(lista)
    text_list = []
    for term in lista:
        if term == "Overall":
            continue
        try:
            text_list.append(dict_types[language][term])
        except:
            text_list.append(term)
        
    f_values = ", ".join(text_list[:-1])
    l_value = text_list[::-1][0]
    if len(text_list) == 1:
        list_values = text_list[0]
    else:
        list_values = {'en': f_values + ' and ' + l_value,
                       'pt': f_values + ' e ' + l_value
                       }
        text_list = list_values[language]
    return text_list
'''

def comment_similar_alerts(metric, direction, similar_list2, dimension):
    similar_list = []
    for term in similar_list2:
        if term == "Overall":
            continue
        try:
            similar_list.append(dict_types[language][term])
        except:
            similar_list.append(term)
        
    f_values = ", ".join(similar_list[:-1])
    l_value = similar_list[::-1][0]
    if len(similar_list) == 1:
        list_values = similar_list[0]
    else:
        list_values = {'en': f_values + ' and ' + l_value,
                       'pt': f_values + ' e ' + l_value
                       }
        list_values = list_values[language]

    dimensions_dict = {'en':{'templates':'templates',
                       'browsers':'browsers',
                       'channels':'channels',
                       'devices':'devices',
                       'traffic types':'traffic types',},
                 'pt':{'templates':'templates',
                       'browsers':'navegadores',
                       'channels':'canais',
                       'devices':'dispositivos',
                       'traffic types':'tipos de tr??fego',}
                 }
    dimension = dimensions_dict[language][dimension]
    
    similar_dict_outliers = {
                'en':{'up':['I found a distortion in <b>%s</b>, the values analyzed were bigger than normal, but it\'s probably not connected to %s, because I found it on %s.<br>' %(metric, dimension, list_values),
                            'I found some high outliers in <b>%s</b>, but there is no connection to %s, because they were found on %s.<br>' %(metric, dimension, list_values),
                            'It\'s possible to see some outliers in <b>%s</b>, but since they are present in %s I believe we can\'t relate it to any effect on %s.<br>' %(metric, list_values, dimension),
                            'I found some big values for <b>%s</b>, but there is no connection to %s, because they were found on %s.<br>' %(metric, dimension, list_values),
                            '%s had high values found in <b>%s</b>, but it\'s not likely to be correlated to %s, otherwise it would happen isolatedly in one of those.<br>' %(list_values, metric, dimension),
                             ],
                      'down':['I found a distortion in <b>%s</b>, the values analyzed were smaller than normal, but it\'s probably not connected to %s, because I found it on %s.<br>' %(metric, dimension, list_values),
                            'I found some low outliers in <b>%s</b>, but there is no connection to %s, because they were found on %s.<br>' %(metric, dimension, list_values),
                            'It\'s possible to see some outliers in <b>%s</b>, but since they are present in %s, I believe we can\'t relate it to any effect on %s.<br>' %(metric, list_values, dimension),
                            'I found some small values for <b>%s</b>, but there is no connection to %s, because they were found on %s.<br>' %(metric, dimension, list_values),
                            '%s had low values found in <b>%s</b>, but it\'s not likely to be not correlated to %s, otherwise it would happen isolatedly in one of those.<br>' %(list_values, metric, dimension),
                            ],
                      },
                'pt':{'up':['Eu encontrei uma distor????o em <b>%s</b>, os valores analisados foram maiores do que o normal, mas provavelmente n??o est?? relacionada com os %s, porque achei isso em %s.<br>' %(metric, dimension, list_values),
                            'Eu achei alguns outliers altos em <b>%s</b>, mas n??o deve haver conex??o com os %s, porque foram encontrados em %s.<br>' %(metric, dimension, list_values),
                            '?? possivel ver alguns outliers em <b>%s</b>, por??m visto que eles aparecem em %s, n??o podemos relacionar isso com nenhum efeito nos %s.<br>' %(metric, list_values, dimension),
                            'Eu encontrei alguns valores grandes para <b>%s</b>, mas n??o h?? conex??o com os %s, pois isso apareceu em %s.<br>' %(metric, dimension, list_values),
                            '%s tiveram valores altos em <b>%s</b>, mas isso provavelmente n??o est?? correlacionado aos %s, sen??o aconteceria isoladamente em algum.<br>' %(list_values, metric, dimension),
                            ],
                      'down':['Eu encontrei uma distor????o em <b>%s</b>, os valores analisados foram menores do que o normal, mas provavelmente n??o est?? relacionada com os %s, porque achei isso em %s.<br>' %(metric, dimension, list_values),
                            'Eu achei alguns outliers baixos em <b>%s</b>, mas n??o deve haver conex??o com os %s, porque foram encontrados em %s.<br>' %(metric, dimension, list_values),
                            '?? possivel ver alguns outliers em <b>%s</b>, por??m visto que eles aparecem em %s, n??o podemos relacionar isso com nenhum efeito nos %s.<br>' %(metric, list_values, dimension),
                            'Eu encontrei alguns valores pequenos para <b>%s</b>, mas n??o h?? conex??o com os %s, pois isso apareceu em %s.<br>' %(metric, dimension, list_values),
                            '%s tiveram valores baixos em <b>%s</b>, mas isso provavelmente n??o est?? correlacionado aos %s, sen??o aconteceria isoladamente em algum.<br>' %(list_values, metric, dimension),],
                      },
                }

    similar_dict_trends = {
                'en':{'rising':['I found a rising trend in <b>%s</b>, but it\'s probably not connected to %s, because I found it on %s.<br>' %(metric, dimension, list_values),
                            '%s are showing a rising trend in <b>%s</b>, but there is probably no relation with %s, otherwise it would happen isolatedly in one of those.<br>' %(list_values, metric, dimension),
                             ],
                      'falling':['I found a falling trend in <b>%s</b>, but it\'s probably not connected to %s, because I found it on %s.<br>' %(metric, dimension, list_values),
                            '%s are showing a falling trend in <b>%s</b>, but there is probably no relation with %s, otherwise it would happen isolatedly in one of those.<br>' %(list_values, metric, dimension),
                             ],
                      },
                'pt':{'rising':['Eu encontrei uma tend??ncia de crescimento em <b>%s</b>, mas n??o deve haver conex??o com os %s, porque foram encontradas em %s.<br>' %(metric, dimension, list_values),
                            '%s est??o mostrando uma tecnd??ncia de crescimento em <b>%s</b>, mas ?? prov??vel que isso n??o tenha rela????o com %s, sen??o aconteceria isoladamente em algum.<br>' %(list_values, metric, dimension),
                             ],
                      'falling':['Eu encontrei uma tend??ncia de queda em <b>%s</b>, mas n??o deve haver conex??o com os %s, porque foram encontradas em %s.<br>' %(metric, dimension, list_values),
                            '%s est??o mostrando uma tend??ncia de queda em <b>%s</b>, mas ?? prov??vel que isso n??o tenha rela????o com %s, sen??o aconteceria isoladamente em algum.<br>' %(list_values, metric, dimension),
                            ],
                      },
                }

    similar_phrase = ''
        
    if direction in ['up','down']:
        similar_phrase += random.choice(similar_dict_outliers[language][direction])
    elif direction in ['rising','falling']:
        similar_phrase += random.choice(similar_dict_trends[language][direction])
    return similar_phrase

def associate_findings(dimension1, dimension2, metric_name1, metric_name2, metric1_dir, metric2_dir, relation):
    try:
        dimension1 = dict_types[languages][dimension1].lower()
        dimension2 = dict_types[languages][dimension2].lower()
    except:
        pass

    directions_dict = {'en':{'up':'up',
                             'rising':'rising',
                             'down':'down',
                             'falling':'falling',
                        },
                       'pt':{'up':'sobe',
                             'rising':'aumenta',
                             'down':'desce',
                             'falling':'diminui',
                           },
        }
    metric1_dir = directions_dict[language][metric1_dir]
    metric2_dir = directions_dict[language][metric2_dir]
    
    metric_comments_1dim_dict = {
        'same':{
        'en':[
              'Normally %s and %s are connected in %s, so it\'s expected to see changes simultaneously on them' %(metric_name1, metric_name2, dimension1),
              'When %s goes %s, %s usually goes %s too. Those KPIs are very connected in %s' %(metric_name1, metric1_dir, metric_name2, metric2_dir, dimension1),
              'As you can see, %s and %s show the same %s movement in %s' %(metric_name1, metric_name2, metric2_dir, dimension1),
              'We can see in %s that %s and %s facing the same behavior quite often' %(dimension1, metric_name1, metric_name2),
              'It is possible that the pointed values in %s %s and %s are related' %(dimension1, metric_name1, metric_name2),
              'When %s has this %s movement in %s, there is a high chance the same %s movement will happen in %s' %(dimension1, metric1_dir, metric_name1, metric2_dir, metric_name2),
              'You can notice %s %s and %s detections are similar' %(dimension1, metric_name1, metric_name2),
              'It is very common to see %s %s and %s with a positive correlation behavior' %(dimension1, metric_name1, metric_name2),
              'There is good chance the %s values found in %s %s have some connection with the %s values in %s' %(metric1_dir, dimension1, metric_name1, metric2_dir, metric_name2),
              'The detected anomalies in %s values for %s and %s are correlated' %(dimension1, metric_name1, metric_name2),
            ],
        'pt':
            [ 'Normalmente %s e %s est??o conectados, ent??o j?? era esperado ver mudan??as similares neles simultaneamente em %s' %(metric_name1, metric_name2, dimension1),
              'Quando %s %s, %s normalmente tamb??m %s. Esses KPIs s??o muito conectados em %s' %(metric_name1, metric1_dir, metric_name2, metric2_dir, dimension1),
              'Como voc?? pode ver, %s e %s mostram o mesmo movimento em %s' %(metric_name1, metric_name2, dimension1),
              'Podemos ver que em %s, %s e %s passam pelo mesmo comportamento com frequ??ncia' %(dimension1, metric_name1, metric_name2),
              'Esse tipo de situa????o normalmente ocorre junto em %s e %s, como vemos em %s' %(metric_name1, metric_name2, dimension1),
              '?? poss??vel que as mudan??as nos valores indicados em %s para %s e %s estejam relacionados' %(dimension1, metric_name1, metric_name2),
              'Quando vemos %s, percebemos um movimento que %s em %s, que tamb??m ocorre em %s' %(dimension1, metric1_dir, metric_name1, metric_name2),
              'Voc?? deve perceber que as detec????es de %s e %s em %s s??o similares' %(metric_name1, metric_name2, dimension1),
              '?? bem comum ver %s e %s em %s com um comportamento de correla????o positivo' %(metric_name1, metric_name2, dimension1),
              'H?? uma boa chance de que o valor que %s encontrado em %s em %s, tenha alguma conex??o com o valor que %s em %s' %(metric1_dir, metric_name1, dimension1, metric2_dir, metric_name2),
              'As anomalias detectadas nos valores de %s em %s e %s est??o correlacionadas' %(dimension1, metric_name1, metric_name2),
            ]},

        'opposite':{
        'en':[
              'Normally %s and %s are connected in %s, so it\'s expected to see opposite changes on them' %(metric_name1, metric_name2, dimension1),
              'When %s goes %s, %s usually goes %s. Those KPIs are very connected in %s' %(metric_name1, metric1_dir, metric_name2, metric2_dir, dimension1),
              'As you can see, %s and %s show the different %s movement in %s' %(metric_name1, metric_name2, metric2_dir, dimension1),
              'We can see in %s that %s and %s facing opposite behavior quite often' %(dimension1, metric_name1, metric_name2),
              'It is possible that the pointed values in %s %s and %s are related' %(dimension1, metric_name1, metric_name2),
              'When %s has this %s movement in %s, there is a high chance an opposite %s movement will happen in %s' %(dimension1, metric1_dir, metric_name1, metric2_dir, metric_name2),
              'You can notice %s %s and %s detections are going in different directions' %(dimension1, metric_name1, metric_name2),
              'It is very common to see %s %s and %s with a negative correlation behavior' %(dimension1, metric_name1, metric_name2),
              'There is good chance the %s values found in %s %s have some connection with the %s values in %s' %(metric1_dir, dimension1, metric_name1, metric2_dir, metric_name2),
              'The detected anomalies in %s values for %s and %s are correlated' %(dimension1, metric_name1, metric_name2),
            ],
        'pt':
            [ 'Normalmente %s e %s est??o conectados, ent??o j?? era esperado ver mudan??as opostas neles simultaneamente em %s' %(metric_name1, metric_name2, dimension1),
              'Quando %s %s, %s normalmente %s. Esses KPIs s??o muito conectados em %s' %(metric_name1, metric1_dir, metric_name2, metric2_dir, dimension1),
              'Como voc?? pode ver, %s e %s mostram movimento diferente em %s' %(metric_name1, metric_name2, dimension1),
              'Podemos ver que em %s, %s e %s passam por comportamentos opostos com frequ??ncia' %(dimension1, metric_name1, metric_name2),
              '?? poss??vel que as mudan??as nos valores indicados em %s para %s e %s estejam relacionados' %(dimension1, metric_name1, metric_name2),
              'Quando vemos esse movimento que %s em %s, existe uma grande chance de que ocorra o inverso em %s' %(metric1_dir, metric_name1, metric_name2),
              'Voc?? deve perceber que as detec????es de %s e %s em %s v??o em dire????es diferentes' %(metric_name1, metric_name2, dimension1),
              '?? bem comum ver %s e %s em %s com um comportamento de correla????o negativo' %(metric_name1, metric_name2, dimension1),
              'H?? uma boa chance de que o valor que %s encontrado em %s em %s, tenha alguma conex??o com o valor que %s em %s' %(metric1_dir, metric_name1, dimension1, metric2_dir, metric_name2),
              'As anomalias detectadas nos valores de %s em %s e %s est??o correlacionadas' %(dimension1, metric_name1, metric_name2),
            ]},
        }

    metric_comments_2dim_dict = {
        'same':{
        'en':[
              'Normally %s %s and %s %s are connected, so it\'s expected to see changes simultaneously on them' %(dimension1, metric_name1, dimension2, metric_name2),
              'When %s %s goes %s, %s %s usually goes %s too' %(dimension1, metric_name1, metric1_dir, dimension2, metric_name2, metric2_dir),
              'You can notice %s %s and %s %s detections are similar' %(dimension1, metric_name1, dimension2, metric_name2),
              'It is very common to see %s %s and %s %s with a positive correlation behavior' %(dimension1, metric_name1, dimension2, metric_name2),
              'There is good chance the %s values found in %s %s have some connection with the %s values in %s %s' %(metric1_dir, dimension1, metric_name1, metric2_dir, dimension2, metric_name2),
            ],
        'pt':
            [ 'Normalmente %s em %s e %s em %s est??o conectados, ent??o j?? era esperado ver mudan??as similares neles simultaneamente' %(metric_name1, dimension1, metric_name2, dimension2),
              'Quando %s em %s %s, normalmente %s em %s %s tamb??m' %(metric_name1, dimension1, metric1_dir, metric_name2, dimension2, metric2_dir),
              'Voc?? deve perceber que as detec????es de %s em %s e %s em %s v??o em dire????es similares' %(metric_name1, dimension1, metric_name2, dimension2),
              '?? bem comum ver %s em %s e %s em %s com um comportamento de correla????o positivo' %(metric_name1, dimension1, metric_name2, dimension2),
              'H?? uma boa chance de que o valor que %s encontrado em %s em %s, tenha alguma conex??o com o valor que %s em %s em %s' %(metric1_dir, metric_name1, dimension1, metric2_dir, metric_name2, dimension2),
            ]},

        'opposite':{
        'en':[
              'Normally %s %s and %s %s are connected, so it\'s expected to see opposite changes on them' %(dimension1, metric_name1, dimension2, metric_name2),
              'When %s %s goes %s, %s %s usually goes %s the opposite' %(dimension1, metric_name1, metric1_dir, dimension2, metric_name2, metric2_dir),
              'You can notice %s %s and %s %s detections are opposite' %(dimension1, metric_name1, dimension2, metric_name2),
              'It is very common to see %s %s and %s %s with a negative correlation behavior' %(dimension1, metric_name1, dimension2, metric_name2),
              'There is good chance the %s values found in %s %s have some connection with the %s values in %s %s' %(metric1_dir, dimension1, metric_name1, metric2_dir, dimension2, metric_name2),
            ],
        'pt':
            [ 'Normalmente %s em %s e %s em %s est??o conectados, ent??o j?? era esperado ver mudan??as opostas neles simultaneamente' %(metric_name1, dimension1, metric_name2, dimension2),
              'Quando %s em %s %s, normalmente %s em %s vai em sentido oposto' %(metric_name1, dimension1, metric1_dir, metric_name2, dimension2),
              'Voc?? deve perceber que as detec????es de %s em %s e %s em %s v??o em dire????es diferentes' %(metric_name1, dimension1, metric_name2, dimension2),
              '?? bem comum ver %s em %s e %s em %s com um comportamento de correla????o negativo' %(metric_name1, dimension1, metric_name2, dimension2),
              'H?? uma boa chance de que o valor que %s encontrado em %s em %s, tenha alguma conex??o com o valor que %s em %s em %s' %(metric1_dir, metric_name1, dimension1, metric2_dir, metric_name2, dimension2),
            ]},
        }
    
    if random.randint(1,100) > 0:
        if dimension1 == dimension2:
            association_phrase = random.choice(metric_comments_1dim_dict[relation][language])
        else:
            association_phrase = random.choice(metric_comments_2dim_dict[relation][language])
        return association_phrase
    
'''    
def hour_interval(begin, end):
    prepositions_dict = {'en':' to ',
                         'pt':' a ',
                        }
    hours_interval = str(begin) + prepositions_dict[language] + str(end)
    return hours_interval
'''

def talk_about_time(exact_time, sign, color):
    sign_text_subs = {'+':{'green':{
                              'en':['improvement','increase','growth','advancement','rise','upgrade','progress'],
                              'pt':['a melhora','o aumento','o crescimento','o avan??o','o upgrade','o progresso'],
                              },
                      'red': {
                              'en':['problem','adversity','growth','rise'],
                              'pt':['o problema','a adversidade','o crescimento','o aumento','a diminui????o'],
                              },
                      'blue':{
                              'en':['change','adjusment','difference','shift','transition','variation','alterations','oscilation','rise'],
                              'pt':['a mudan??a','o ajuste','a modifica????o','a altera????o','a transi????o','a varia????o','a oscila????o','o aumento'],
                              },
                      },
                 '-':{'green':{
                              'en':['improvement','advancement','upgrade','progress','fall','reduction'],
                              'pt':['a melhora','o avan??o','o upgrade','o progresso','a queda','a redu????o'],
                              },
                      'red': {
                              'en':['decrement','decline','fall','problem','reduction','adversity'],
                              'pt':['o decr??scimo','o decl??nio','a queda','o problema','a piora','a redu????o','a adversidade'],
                              },
                      'blue':{
                              'en':['change','adjusment','difference','shift','transition','variation','alterations','oscilation','rise'],
                              'pt':['a mudan??a','o ajuste','a modifica????o','a altera????o','a transi????o','a varia????o','a oscila????o','o aumento'],
                              },
                      }
                 }

    substantive_change_word = random.choice(sign_text_subs[sign][color][language])
    time_possibilities_dict = {
                              'en':['It\'s likely the %s occured at %s.<br>' %(substantive_change_word, exact_time),
                                    'The biggest %s occured at %s.<br>' %(substantive_change_word, exact_time),
                                    'The recorded values suggest that it happened at %s.<br>' %exact_time,
                                    'The greatest value change was at %s.<br>' %exact_time,
                                    'It could have happened at %s due to this big %s we had.<br>' %(exact_time, substantive_change_word),
                                    'I would say it started at %s because I found a big %s at this time.<br>' %(exact_time, substantive_change_word),
                                    ],
                              
                          'pt':['?? prov??vel que %s tenha ocorrido ??s %s.<br>' %(substantive_change_word, exact_time),
                                'Dentre tudo que foi identificado, %s mais relevante foi em %s.<br>' %(substantive_change_word, exact_time),
                                'Os valores registrados sugerem que isso foi em %s.<br>' %exact_time,
                                'A maior mudan??a de valor foi em %s.<br>' %exact_time,
                                'Isso pode ter acontecido em %s j?? que %s mais significante foi essa hora.<br>' %(exact_time, substantive_change_word),
                                'Eu diria que isso come??ou em %s porque %s ocorre nessa hora.<br>' %(exact_time, substantive_change_word),
                                ],
                         }

    possibility_phrase = random.choice(time_possibilities_dict[language])
    return possibility_phrase
    
# -------------------------------------------- GREETINGS PART --------------------------------------------------
def get_random_texts(name_greetings, email_issues):
    talk_hour = int(current_send_hour.split(':')[0])
    if talk_hour >= 5 and talk_hour < 13:
        dict_hour_greetings = {'en':'Good Morning',
                               'pt':'Bom dia',}
    elif talk_hour >= 13 and talk_hour < 19:
        dict_hour_greetings = {'en':'Good Afternoon',
                               'pt':'Boa tarde',}
    elif talk_hour >= 19 or talk_hour < 5:
        dict_hour_greetings = {'en':'Good Night',
                               'pt':'Boa noite',}
    talk_hour = dict_hour_greetings[language]
    
    if name_greetings != "general":
        name_greetings = name_greetings.split(',')
        name = random.choice(name_greetings)

        grettings = {
                'en':
                    ["Hi %s," %name,
                     "Hello %s," %name,
                     "Hi %s! How have you been?" %name,
                     "How have you been %s?" %name,
                     "Hey %s!" %name,
                     "Hey %s! What's up?" %name,
                     "How are you doing %s?" %name,
                     "Hello %s! How are you doing?" %name,
                     "%s %s!" %(talk_hour, name),
                     "Hi %s, how are you?" %name,
                     "Hello %s, how are you?" %name,
                     "How???s your day %s?" %name,
                     "%s! How do you do?" %name,
                     "Are you allright %s?" %name,
                     "%s! Are you ok?" %name,
                    ],
                'pt':
                    ["Oi %s," %name,
                     "Ol?? %s," %name,
                     "%s %s! Como voc?? est???" %(talk_hour, name),
                     "Como voc?? est?? %s?" %name,
                     "Ei %s!" %name,
                     "E a?? %s!? Tudo bem?" %name,
                     "Como voc?? est?? %s?" %name,
                     "Ol?? %s! Voc?? est?? bem?" %name,
                     "%s %s!" %(talk_hour, name),
                     "Oi %s, voc?? est?? bem?" %name,
                     "Ol?? %s, como vai?" %name,
                     "Como vai %s?" %name,
                     "%s! Tudo certo?" %name,
                     "Tudo certo com voc??, %s?" %name,
                     "%s! Est?? tudo bem?" %name,
                    ],
                }
        
    else:
        grettings = {
                'en':
                    ["Hi,",
                     "Hello,",
                     "Hi everyone,",
                     "Hello everyone,",
                     "Hi guys,",
                     "Hi there,",
                     "Hello guys,",
                     "Hi! How have you been?",
                     "How have you been?",
                     "Hey!",
                     "What's up?",
                     "Hey! What's up?",
                     "How are you doing?",
                     "Hello! How are you doing?",
                     "Greetings!",
                     "%s!" %talk_hour,
                     "Hi, how are you?",
                     "Hello, how are you?",
                     "Hey people!",
                     "How???s your day?",
                     "How do you do?",
                     "Are you allright?",
                     "Are you ok?",
                     ],
                'pt':
                    ["Oi,",
                     "Ol??,",
                     "%s pessoal," %talk_hour,
                     "%s a todos," %talk_hour,
                     "Oi pessoal,",
                     "Ol?? pessoal,",
                     "Oi! Como voc??s est??o?",
                     "Como voc??s est??o?",
                     "Ei!",
                     "E a???",
                     "E a??! Tudo bem?",
                     "Voc?? est?? bem?",
                     "Ol??! Tudo certo com voc???",
                     "Oi! Est?? tudo bem com voc??s?",
                     "%s!" %talk_hour],
                    }

    if email_issues == 'just_alert':
        # ------------------------------------------- INTRODUCTIONS PART ---------------------------------------------
        introductions1 = {
                    'en':
                        ["I found some interesting stuff in my last analysis, ",
                         "There are some surprising things in the data I was looking at, ",
                         "I gathered some data for you, ",
                         "I do need to tell you some stuff, ",
                         "I believe you may be interested in what I found out, ",
                         "I had some insights in my last data analysis, " ,
                         "This data seems to show some unusual values, " ,
                         "My last analysis may be of your interest, ",
                         "I saw something you may be interested in, " ,
                         "I have some news for you, " ,
                         "There is something different from expected in the following data, ",
                         "After my last analysis I had some conclusions, " ,
                         "I found some distortions in the data I was analyzing, " ,
                          ],
                    'pt':
                        ["Eu encontrei algumas coisas interessantes na minha ??ltima an??lise, ",
                         "Existem algumas coisas surpreendentes nos dados que eu estava olhando, ",
                         "Eu coletei alguns dados para voc??, ",
                         "Eu preciso te falar sobre algumas coisas que encontrei na minha ??ltima an??lise, ",
                         "Eu acredito que voc?? possa ter interesse nos dados que eu encontrei, ",
                         "Eu tive algumas ideas depois de fazer minha ??ltima an??lise, " ,
                         "Separei alguns dados que est??o apresentando valores incomuns, " ,
                         "Eu vi algumas coisas nas quais voc?? pode ter interesse, " ,
                         "Eu tenho algumas novidades para voc??, " ,
                         "Existem algumas coisas diferentes do esperado nos valores abaixo, ",
                         "Depois da minha ??ltima an??lise eu cheguei em algumas conclus??es, " ,
                         "Eu encontrei algumas distor????es nos dados que estava analisando, " ,
                          ],
                        }

        introductions2 = {
                    'en':
                        ["you should take a look at the information below.",
                         "so I thought about sharing it with you.",
                         "so I decided to share it with you.",
                         "so I created this report you.",
                         "and I believe this information can be useful to you.",
                         "let me go over some points.",
                         "we should see the following topics.",
                         "you can always count on me!" ,
                         "I hope this can help you somehow." ,
                         "I hope this can help you." ,
                         "perhaps we can use this information." ,
                         "consider analyzing this." ,
                         "you should consider seing it." ,
                         "please consider analyzing it." ,
                         "check this out.",
                         "check this report.",
                         "check out what I have for you.",
                         "take a look in what I've separated for you.",
                         "take a look at this." ,
                         "please take a look at this." ,
                         "did you see this?" ,
                         "let me summarize what I've discovered." ,
                         "let me summarize some points."
                        ],
                     'pt':
                        ["voc?? deveria dar uma olhada nos dados abaixo.",
                         "ent??o pensei em compartilhar isso com voc??.",
                         "ent??o decidi em compartilhar isso com voc??.",
                         "ent??o eu criei esse relat??rio para voc??.",
                         "e eu acredito que essa informa????o pode ser ??til para voc??.",
                         "deixe-me passar por alguns pontos.",
                         "acho v??lido vermos os seguintes t??picos.",
                         "espero que isso possa te ajudar de alguma forma." ,
                         "espero que isso possa te ajudar." ,
                         "talvez n??s possamos usar essa informa????o." ,
                         "considere analisar isso." ,
                         "voc?? devia considerar ver isso." ,
                         "por favor considere analisar isso." ,
                         "d?? uma olhada nisso.",
                         "veja esse relat??rio.",
                         "veja o que eu separei para voc??.",
                         "veja isso." ,
                         "por favor de uma olhada nisso." ,
                         "voc?? viu isso?" ,
                         "vou resumir o que eu descobri." ,
                         "vou resumir em alguns t??picos."
                        ],
                    }

        # -------------------------------------------- ENDINGS PART ---------------------------------------------------
        endings1 = {
                'en':
                    ["I'll keep monitoring, ",
                    "I'm always watching for your data, ",
                    "On my side I'll make more analysis, ",
                    "On my side I'll keep on checking the data, ",
                    "I am going back to make further analysis of your data, ",
                    "I hope you found it useful, ",
                    "I'll try to find more information, " ,
                    "I hope I could make the points clear, " ,
                    "I hope you can make good use of this, " ,
                    "There is always something to watch out of the radar, " ,
                    "I'll keep you informed, " ,
                    "I'll report if I find anything else, " ,
                    "I'll get in touch with you if I find more interesting data, " ,
                    "Just as you know, " ,
                    "As you may expect, " ,
                    "I'll get back to my analysis cycle, " ,
                    "Lastly, " ,
                    "In case anything else happens, I'll let you know, ",
                    "I'll tell you whenever I find something out of order, ",
                    "Let's keep on watching these data, ",
                    "Whenever there is something new I'll let you know, ",
                    "This is what I could find for now, ",
                    "I'll continue checking for anomalies, ",
                    ],
                 'pt':
                    ["Vou seguir monitorando, ",
                    "Estou sempre atento a seus dados, ",
                    "Do meu lado, vou fazer mais an??lises, ",
                    "Do meu lado, seguirei verificando os dados, ",
                    "Eu vou continuar fazendo outras an??lises dessas informa????es, ",
                    "Eu espero que as informa????es tenham sido ??teis, ",
                    "Eu vou tentar encontrar mais informa????es, " ,
                    "Eu espero ter deixado esses pontos claros, " ,
                    "Eu espero que voc?? possa fazer bom uso disso, " ,
                    "Sempre existe algo fora do radar para ser observado, " ,
                    "Eu vou me manter te informando, " ,
                    "Eu te informarei caso encontre algo a mais, " ,
                    "Entrarei em contato com voc?? caso eu encontre mais alguma informa????o interessante, " ,
                    "Como voc?? sabe, " ,
                    "Como voc?? deve esperar, " ,
                    "Eu voltarei para meu ciclo de an??lises, " ,
                    "Por fim, " ,
                    "Caso algo mais aconte??a, eu te aviso, ",
                    "Eu avisarei sempre que encontrar algo desse tipo fora de ordem, ",
                    "Vamos seguir monitorando esses dados, ",
                    "Sempre que houver algo novo, eu o avisarei, ",
                    "Isso ?? o que eu pude encontrar at?? o momento, ",
                    "Eu vou continuar procurando por anomalias, ",
                    ],
                }

        endings2 = {
                'en':
                    ["you can contact Simplex team if you have any doubts." ,
                    "don't hesitate to ask me anything in case you need it.",
                    "please tell me if you need anything else.",
                    "please contact me if you need more details." ,
                    "fell free to contact me.",
                    "fell free to ask me for further information.",
                    "keep in mind I'm at your disposal." ,
                    "tell me if you need more details." ,
                    "tell me in case you need some assistance." ,
                    "talk to me if you feel like you need more info." ,
                    "talk to me in case you need a further explanation." ,
                    "you can always ask me for more stuff." ,
                    "let me know if I can help you in something else." ,
                    "you can contact me anyway." ,
                    "don't bother to ask me anything else you need.",
                    "don't bother to ask me more information." ,
                    "I'm always ready to give you assistance." ,
                    "I'm always at your disposal." 
                    ],
                'pt':
                    ["voc?? pode entrar em contato com a equipe da Simplex se tiver alguma d??vida." ,
                    "n??o hesite em me perguntar qualquer coisa que voc?? precise.",
                    "por favor me diga se voc?? ainda precisa de algo.",
                    "por favor me contate se voc?? precisar de mais detalhes." ,
                    "fique a vontade para me contatar.",
                    "fique a vontade para me perguntar por mais informa????es.",
                    "saiba que estou a sua disposi????o." ,
                    "me diga se voc?? precisar de mais detalhes." ,
                    "me diga se voc?? precisar de alguma ajuda." ,
                    "fale comigo se sentir que precisa de mais informa????es." ,
                    "fale comigo caso voc?? precise de alguma explica????o mais detalhada." ,
                    "voc?? sempre pode me pedir mais informa????es." ,
                    "me avise se eu ainda puder te ajudar." ,
                    "voc?? pode entrar em contato comigo sempre." ,
                    "n??o se incomode de me perguntar qualquer coisa que precisar.",
                    "n??o se incomode em me pedir por mais informa????es." ,
                    "estou sempre pronto para lhe oferecer ajuda." ,
                    "estou sempre a sua disposi????o." 
                    ],
                }
    elif email_issues == 'just_report':
        # ------------------------------------------- INTRODUCTIONS PART ---------------------------------------------
        introductions1 = {
                    'en':
                        ["You can see below the KPIs you setup to follow.",
                         "The requested KPIs are available in the graphs below.",
                         "You can see below the data you setup to follow.",
                         "The requested data is available in the graphs below.",
                         "I'll keep you informed with the information you asked for.",
                         "Take a look in the information you setup to receive.",
                         "Take a look in the information you setup to follow.",
                         "The reports you requested are available below.",
                         "Here it is your requested report.",
                          ],
                    'pt':
                        ["Verifique abaixo os seus KPIs configurados para monitoramento.",
                         "Os KPIs requisitados est??o dispon??veis nos gr??ficos abaixo.",
                         "Verifique abaixo os dados que foram configurados para monitoramento.",
                         "Os dados requisitados est??o dispon??veis nos gr??ficos abaixo.",
                         "Te manterei informado sobre as informa????es que voc?? pediu para seguir.",
                         "Aqui est??o as informa????es que voc?? configurou para receber.",
                         "Aqui est??o as informa????es que voc?? configurou para seguir.",
                         "Aqui est?? o seu relat??rio de acompanhamento",
                         "Aqui est?? o relat??rio requisitado.",
                          ],
                        }

        introductions2 = {
                    'en':
                        ["","","","","",
                         " Take a look.",
                         " Check it out.",
                         " All the values from the analysis look good.",
                         " All the values from the data are according to my expectations.",
                         " I couldn't detect any distortions in the data.",
                         " I couldn't see anything out of order.",
                         " I didn't find anything out of normal in the data.",
                         " It seems the data is showing values according to my expectations.",
                         " There are no surprises in the data I checked.",
                         " There is nothing unexpected in the report.",
                         " The values analyzed remain in the same baseline.",
                         " Everything just keeps on inside normal values today.",
                         " Everything is showing normal behavior today.",
                         " I believe there is nothing out of control regarding the last values.",
                         " Taking in consideration the last values, I believe everything is under control.",
                         " Just to let you know, there is nothing wrong the the values analyzed.",
                         ],
                     'pt':
                        ["","","","","",
                         " D?? uma olhada.",
                         " N??o deixe de ver.",
                         " Confira.",
                         " Todos os valores analizados parecem normais.",
                         " Todos os dados est??o de acordo com minhas expectativas.",
                         " Hoje n??o h?? nenhum valor fora da curva nos dados",
                         " Eu n??o pude detectar nenhuma distor????o nos dados.",
                         " Eu n??o encontrei nada fora de ordem.",
                         " Eu n??o encontrei nada fora do normal nos valores.",
                         " Parece que os dados est??o de acordo com o esperado.",
                         " N??o h?? surpresas nos dados que eu olhei.",
                         " N??o h?? nada de inesperado no relat??rio.",
                         " Os valores avaliados seguem no mesmo patamar.",
                         " Tudo se mant??m dentro de valores normais.",
                         " Tudo apresenta comportamento normal.",
                         " Eu acredito que n??o haja nada fora de controle relacionado aos ??ltimos valores.",
                         " Levando em considera????o os ??ltimos valores, eu acredito que tudo esteja sobre controle.",
                         " Para que voc?? saiba, n??o h?? nada de errado nos valores analisados.",
                        ],
                    }
        introductions2 = {'en':[""],'pt':[""]}

        # -------------------------------------------- ENDINGS PART ---------------------------------------------------
        endings1 = {
                'en':
                    ["I'll keep on sending you the data, ",
                     "I'll keep on bringing you this information, ",
                     "I'll keep on monitoring, ",
                     "I'll continue monitoring, ",
                     "I'll continue following these values, ",
                     "Lastly, " ,
                     "Let's carry on watching this, " ,
                    ],
                 'pt':
                    ["Vou seguir enviando os dados, ",
                     "Vou seguir trazendo os dados para voc??, ",
                     "O monitoramento continuar?? sendo enviado a voc??, ",
                     "Seguirei te informando, ",
                     "Por fim, " ,
                     "Vamos continuar acompanhando, " ,
                     "Seguirei acompanhando, " ,
                    ],
                }

        endings2 = {
                'en':
                    ["you can contact Simplex team if you have any doubts." ,
                    "I'm always at your disposal." ,
                    "please tell me if you need anything else.",
                    "please contact me if you need more details." ,
                    "fell free to contact me.",
                    "fell free to ask me for further information.",
                    "keep in mind I'm at your disposal." ,
                    "tell me if you need more details." ,
                    "tell me in case you need some assistance." ,
                    "talk to me if you feel like you need more info." ,
                    "let me know if I can help you in something else." ,
                    "let's hope everything stays under control." ,
                    "in case anything happens, I'll let you know." ,
                    ],
                'pt':
                    ["voc?? pode entrar em contato com a equipe da Simplex se tiver alguma d??vida." ,
                    "estou sempre a sua disposi????o.",
                    "por favor me diga se voc?? precisa de algo a mais.",
                    "por favor me contate se voc?? precisar de mais informa????es." ,
                    "fique a vontade para me contatar.",
                    "fique a vontade para me perguntar por mais informa????es.",
                    "saiba que estou a sua disposi????o." ,
                    "me diga se voc?? precisar de mais detalhes." ,
                    "me diga se voc?? precisar de alguma ajuda." ,
                    "fale comigo se sentir que precisa de mais informa????es." ,
                    "me avise se eu puder te ajudar em algo a mais." ,
                    "estou sempre a sua disposi????o." 
                    ],
                }
    elif email_issues == 'alert_and_report':
        # ------------------------------------------- INTRODUCTIONS PART ---------------------------------------------

        ###
        ##
        ##
        ##
        introductions1 = {
                    'en':
                        ["I found some interesting stuff in my last analysis, ",
                         "Simplex is always watching for you data, " 
                          ],
                    'pt':
                        ["Eu encontrei algumas coisas interessantes na minha ??ltima an??lise, ",
                         "A Simplex est?? sempre monitorando seus dados, " 
                          ],
                        }

        introductions2 = {
                    'en':
                        ["you should take a look at the information below.",
                         "let me summarize some points."
                        ],
                     'pt':
                        ["voc?? deveria dar uma olhada nos dados abaixo.",
                         "ent??o pensei em compartilhar isso com voc??.",
                        ],
                    }

        # -------------------------------------------- ENDINGS PART ---------------------------------------------------
        endings1 = {
                'en':
                    ["I'll keep monitoring, ",
                    "Lastly, " ,
                    ],
                 'pt':
                    ["Vou seguir monitorando, ",
                    "Por fim, " ,
                    ],
                }

        endings2 = {
                'en':
                    ["you can contact Simplex team if you have any doubts." ,
                    "let me know if I can help you in something else." ,
                    ],
                'pt':
                    ["voc?? pode entrar em contato com a equipe da Simplex se tiver alguma d??vida." ,
                    "estou sempre a sua disposi????o." 
                    ],
                }

    # ------------------------------------- GOODBYES PART -----------------------------------------------
    goodbyes = {
            'en':
                ["Regards",
                "Goodbye",
                "See you",
                "See you later",
                "Until next time",
                "I've got go",
                "I've got get going",
                "Have a nice day",
                "Take care of yourself",
                "Take care",
                "Bye",
                "See you next time",
                "It was nice to help to you",
                "It was nice to talk to you",
                ],
            'pt':
                ["Atenciosamente",
                "Abra??o",
                "Abra??os",
                "At?? mais",
                "At?? a pr??xima vez",
                "Agrade??o a aten????o",
                "Obrigado",
                "Grato",
                "Att",
                "At?? breve",
                "At?? ?? pr??xima",
                ],
            }

    chosen_grettings = random.choice(grettings[language])
    chosen_introduction = random.choice(introductions1[language]) + random.choice(introductions2[language])
    chosen_ending = random.choice(endings1[language]) + random.choice(endings2[language])
    chosen_goodbye = random.choice(goodbyes[language])
    return chosen_grettings, chosen_introduction, chosen_ending, chosen_goodbye
