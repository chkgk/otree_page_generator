from otree_tg import Experiment


def main():
    exp = Experiment('Example.docx')

    for page in exp.pages:
        print(page.render_page_class())
        print(page.render_template())

    if exp.player_fields:
        print(exp.render_player_class())

    if exp.group_fields:
        print(exp.render_group_class())


if __name__ == '__main__':
    main()
