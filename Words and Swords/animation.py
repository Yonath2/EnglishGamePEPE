class Animation:
    def __init__(self, frames):
        self.frames = frames  # images de l'animation
        self.length = len(self.frames)  # longueur de l'animation (le nombre de frames)
        self.current_frame = 0
        self.instance = 0

    def play(self, new_state, speed, repeat=0):  # plus speed est élevé, plus l'animation est lente
        if self.current_frame + 1 >= self.length * speed:  # vrai si un cycle d'animation est fini
            if repeat == -1:
                self.instance += 1
                self.current_frame = 0

            elif self.instance < repeat:
                self.instance += 1
                self.current_frame = 0
            else:
                return new_state
        frame = self.frames[self.current_frame // speed]
        self.current_frame += 1
        return frame

    def reset(self):
        self.current_frame = 0
        self.instance = 0






















