from Spells import *
from Monsters import *
from Upgrades import FarmiliarSkill, skill_constructors

def summon_farmiliar_cooldown(self):
    self.farmiliar = self.make_farmiliar()
    apply_minion_bonuses(self, self.farmiliar)
    self.counter_max += 3
    self.summon(self.farmiliar)


class WizardingInternFamiliar(FarmiliarSkill):
    def __init__(self):
        FarmiliarSkill.__init__(self)
        self.counter_max = 10
        self.counter = self.counter_max
        self.minion_health = 25
        self.minion_damage = 5
        self.minion_range = 10

        self.name = "Wizarding Intern"
        self.description = ("Every [{counter_max}:minion_duration] turns, summon a wizard intern if you do not currently have one.\n"
                            "The intern has a simple arcane ranged attack.\n"
                            "The familiar can cast your sorcery cantrips on a 7 turn cooldown.\n"
                            "Every time your intern dies, the next intern takes three turns longer to summon.").format(counter_max = self.counter_max)
        self.level = 4
        self.tags = [Tags.Conjuration]

    def get_extra_examine_tooltips(self):
        return [WizardingIntern()]

    def make_farmiliar(self):
        monster = WizardingIntern()

        for spell in reversed(self.owner.spells):
            if spell.level == 1 and Tags.Sorcery in spell.tags:
                intern_spell = type(spell)()
                intern_spell.statholder = self.owner
                intern_spell.max_charges = 0
                intern_spell.cur_charges = 0
                intern_spell.cool_down = 7

                monster.spells.insert(0, intern_spell)

        return monster
    
    def summon_farmiliar(self):
        self.counter_max += 3
        self.description = ("Every [{counter_max}:minion_duration] turns, summon a wizard intern if you do not currently have one.\n"
                            "The intern has a simple arcane ranged attack.\n"
                            "The familiar can cast your sorcery cantrips on a 7 turn cooldown.\n"
                            "Every time your intern dies, the next intern takes three turns longer to summon.").format(counter_max = self.counter_max)
        return super().summon_farmiliar()
    
    def on_enter_level(self, evt):
        self.counter_max = 10
        self.counter = 10
        self.description = self.description = ("Every [{counter_max}:minion_duration] turns, summon a wizard intern if you do not currently have one.\n"
                            "The intern has a simple arcane ranged attack.\n"
                            "The familiar can cast your sorcery cantrips on a 7 turn cooldown.\n"
                            "Every time your intern dies, the next intern takes three turns longer to summon.").format(counter_max = self.counter_max)
        

def WizardingIntern():

    unit = Unit()
    unit.max_hp = 25

    unit.name = "Wizard Intern"

    unit.asset = ["WizardingIntern","intern"]

    basic_attack = SimpleRangedAttack(damage=5, beam=False, range=10, damage_type=Tags.Arcane, cool_down=5)
    basic_attack.name = "Junior Magic Missile"
    unit.spells = [basic_attack]
    unit.tags = [Tags.Living]

    return unit

skill_constructors.append(WizardingInternFamiliar)