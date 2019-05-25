def lugar(janela, botao_play, botao_playhover, botao_dificuldade, botao_dificuldadehover, botao_rank, botao_rankhover, botao_quit, botao_quithover):

    botao_play.set_position((janela.width / 2) - (botao_play.width / 2), (janela.height / 4) - botao_play.height)
    botao_playhover.set_position(botao_play.x, botao_play.y)

    botao_dificuldade.set_position((janela.width / 2) - (botao_dificuldade.width / 2), (janela.height / 4) - botao_dificuldade.height + 100)
    botao_dificuldadehover.set_position(botao_dificuldade.x, botao_dificuldade.y)

    botao_rank.set_position((janela.width / 2) - (botao_rank.width / 2), (janela.height / 4) - botao_rank.height + 200)
    botao_rankhover.set_position(botao_rank.x, botao_rank.y)

    botao_quit.set_position((janela.width / 2) - (botao_quit.width / 2), (janela.height / 4) - botao_quit.height + 300)
    botao_quithover.set_position(botao_quit.x, botao_quit.y)

