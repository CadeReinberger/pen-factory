from numpy.random import choice
from configs import PACKET_LENGTH

category_data = [(14, 'Mythology', .7), (15, 'Literature', 4.1), (16, 'Trash', 2.4), (17, 'Science', 5.6), (18, 'History', 4.8), (19, 'Religion', .6), (20, 'Geography', 1.8), (21, 'Fine Arts', 1.6), (22, 'Social Science', .7), (25, 'Philosophy', .5), (26, 'Current Events', 1.2)] #current events is slightly nerfed since it's hard on old sets. Since it is practice, it's been given to trash
cat_dict = dict([x[:2] for x in category_data])

#Unused for the forseeable future. 
#subcategory_data = [[(1, 'Literature European', 15), (2, 'Fine Arts Visual', 21), (4, 'Literature American', 15), (5, 'Science Chemistry', 17), (6, 'History British', 18), (8, 'Fine Arts Auditory', 21), (10, 'Science Other', 17), (13, 'History American', 18), (14, 'Science Biology', 17), (16, 'History Classical', 18), (18, 'Science Physics', 17), (20, 'History World', 18), (22, 'Literature British', 15), (23, 'Science Computer Science', 17), (24, 'History European', 18), (25, 'Fine Arts Other', 21), (26, 'Science Math', 17), (27, 'Fine Arts Audiovisual', 21), (28, 'History Other', 18), (29, 'Literature Other', 15), (30, 'Literature Classical', 15), (31, 'Religion American', 19), (32, 'Trash American', 16), (33, 'Mythology American', 14), (34, 'Social Science American', 22), (35, 'Fine Arts American', 21), (36, 'Science American', 17), (37, 'Science World', 17), (38, 'Geography American', 20), (39, 'Philosophy American', 25), (40, 'Current Events American', 26), (42, 'Current Events Other', 26), (43, 'Fine Arts World', 21), (44, 'Geography World', 20), (45, 'Fine Arts British', 21), (46, 'Mythology Indian', 14), (47, 'Mythology Chinese', 14), (49, 'Mythology Other East Asian', 14), (48, 'Mythology Japanese', 14), (50, 'Fine Arts European', 21), (51, 'Religion East Asian', 19), (52, 'Philosophy East Asian', 25), (53, 'Trash Video Games', 16), (54, 'Mythology Other', 14), (55, 'Trash Sports', 16), (56, 'Social Science Economics', 22), (57, 'Religion Christianity', 19), (58, 'Mythology Greco-Roman', 14), (59, 'Trash Other', 16), (60, 'Social Science Other', 22), (61, 'Philosophy Classical', 25), (12, 'Literature World', 15), (62, 'Religion Other', 19), (63, 'Mythology Norse', 14), (64, 'Social Science Political Science', 22), (65, 'Mythology Egyptian', 14), (66, 'Philosophy European', 25), (67, 'Trash Music', 16), (68, 'Religion Islam', 19), (69, 'Religion Judaism', 19), (70, 'Trash Television', 16), (71, 'Social Science Psychology', 22), (72, 'Trash Movies', 16), (73, 'Social Science Sociology', 22), (74, 'Philosophy Other', 25), (75, 'Social Science Linguistics', 22), (76, 'Social Science Anthropology', 22), (77, 'Fine Arts Opera', 21)]]

tot = sum([x[2] for x in category_data])
choices = [x[0] for x in category_data]
probs = [x[2]/tot for x in category_data]


def gen_random_game():
    c = choice(choices, size=(PACKET_LENGTH), p=probs)
    return c

def validate_rand_game(game):
    game = list(game)
    #asserts at least 3 of each of the big 3 and no back-backs
    enough_lit = game.count(15) >= 3
    enough_hist = game.count(18) >= 3
    enough_sci = game.count(17) >= 3
    back_to_back = any([game[i] == game[i+1] for i in range(0, PACKET_LENGTH-1)])
    return enough_lit and enough_hist and enough_sci and not back_to_back

def make_round():
    while True:
        rd = gen_random_game()
        if validate_rand_game(rd):
            return rd
        
def make_game():
    return (make_round(), make_round())