from otree_tg import Experiment
from otree_tg.adapters import WordAdapter


def main():
    wa = WordAdapter('test_data/Example.docx')
    exp = Experiment(wa)

    if exp.player_fields:
        print(exp.render_player_class())

    if exp.group_fields:
        print(exp.render_group_class())

    for page in exp.pages:
        print(page.render_class())
        print(page.render_template())


if __name__ == '__main__':
    main()
