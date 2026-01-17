import pyxel

# ===== 定数定義 =====
SCREEN_W = 140
SCREEN_H = 150
PAD_W = 16
PAD_H = 8
BALL_W = 5
BALL_H = 5
BALL_R = BALL_W // 2

MAX_LIFE= 5
BLOCK_COLS = 8
BLOCK_ROWS = 3
BLOCK_W = 16
BLOCK_H = 8
BLOCK_X0 = 5
BLOCK_Y0 = 8
# ===== ゲーム状態 =====
PLAY  = 0
OVER  = 1
CLEAR = 2
TITLE = 3
MISS  = 4

class App:
    def __init__(self):

        pyxel.init(SCREEN_W, SCREEN_H, title="Pyxel Brick Breaker")
        pyxel.mouse(False)
        pyxel.load("block.pyxres")

        self.game_state=TITLE
        self.score=0
        self.ball_life=MAX_LIFE
        self.block_count=BLOCK_ROWS * BLOCK_COLS
        self.blocks = [[1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1]]
        self.pad_x = SCREEN_W // 2 - PAD_W //2
        self.pad_y = SCREEN_H - 16
        self.ball_x = self.pad_x + 5
        self.ball_y = self.pad_y - BALL_H
        self.vx = 2
        self.vy = -2
       
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_state==PLAY:
            # パドルの移動
            if pyxel.btn(pyxel.KEY_LEFT):
                self.pad_x = max(0, self.pad_x - 2)
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.pad_x = min(pyxel.width - PAD_W, self.pad_x + 2)

            # ボールの移動
            self.ball_x += self.vx
            self.ball_y += self.vy

            # 壁との衝突判定
            if self.ball_x <= 0:
                self.ball_x=0
                self.vx *= -1
            elif self.ball_x >=  SCREEN_W - BALL_W:
                self.ball_x = SCREEN_W - BALL_W
                self.vx *= -1
            if self.ball_y<=0:
                self.ball_y=0
                self.vy *= -1
        
            # パドルとの衝突判定
            if (
                self.ball_y + BALL_H >= self.pad_y and
                self.vy>0 and
                self.pad_x - BALL_R <= self.ball_x <= self.pad_x + PAD_W + BALL_R):
                self.ball_y = self.pad_y - 4
                self.vy *= -1
                #端に当たるとスピードアップ
                if (self.ball_x<=self.pad_x+2 and self.ball_x>BALL_W*1.5):
                    abs_i=abs(self.vx)+1
                    self.vx=abs_i
                    abs_i=abs(self.vy)+1
                    self.vy = -abs_i
                elif (self.ball_x>=self.pad_x+PAD_W-2 and self.ball_x<SCREEN_W-BALL_W*1.5):
                    abs_i=abs(self.vx)+1
                    self.vx=-abs_i
                    abs_i=abs(self.vy)+1
                    self.vy=-abs_i

            # ブロックとの衝突判定
            # ボールの中心付近の座標から、ブロック配列のどこに位置するか計算
            # ブロックの描画開始位置を考慮
            bx = (self.ball_x + BALL_W//2 - BLOCK_X0) // BLOCK_W
            by = (self.ball_y + BALL_H - BLOCK_Y0) // BLOCK_H

            if 0 <= by < len(self.blocks) and 0 <= bx < len(self.blocks[0]):
                if self.blocks[by][bx] == 1:
                    self.blocks[by][bx] = 0 # ブロックを消す
                    self.block_count-=1
                    self.vy *= -1          # 跳ね返る
                    self.score+=10
                    #Clear判断
                    if self.block_count==0:
                        self.game_state=CLEAR

            # ミス判定（画面下に落ちたらリセット）
            if self.ball_y > SCREEN_H:
                self.game_state=MISS
                self.ball_life-=1
                self.ball_x = self.pad_x+5
                self.ball_y=self.pad_y-4
                self.vy = -2

        elif self.game_state==OVER:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.restart()
                self.game_state=PLAY
        elif self.game_state==CLEAR:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            elif pyxel.btnp(pyxel.KEY_SPACE):
                self.restart()
                self.game_state=PLAY
        elif self.game_state==TITLE:  #title
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            elif pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.restart()
                self.game_state=PLAY
        elif self.game_state==MISS and self.ball_life>0:  #miss
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            elif pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.vx=2
                self.vy=-2
                self.game_state=PLAY
        elif self.ball_life==0:
            self.game_state=OVER
    
    def restart(self):
        self.block_count=BLOCK_ROWS*BLOCK_COLS
        self.score=0
        self.ball_life=MAX_LIFE
        self.pad_x = SCREEN_W // 2 - PAD_W//2
        self.pad_y = SCREEN_H - 16
        self.ball_x = self.pad_x + 5
        self.ball_y = self.pad_y - 4
        self.vx = 2
        self.vy = -2

        for i in range(BLOCK_ROWS):
            for j in range(BLOCK_COLS):
                self.blocks[i][j] = 1

    def draw(self):
        pyxel.cls(0)
        # Score
        pyxel.text(2,0,f"SCORE:{self.score}",7)
        pyxel.text(pyxel.width-30,0,f"BALL:{self.ball_life}",7)
      
        # ブロックの描画
        for i in range(BLOCK_ROWS):
            for j in range(BLOCK_COLS):
                if self.blocks[i][j] == 1:
                    bltPos = 8 if j % 2 == 0 else 24
                    # 座標計算をupdateの判定と合わせる
                    pyxel.blt(j * 16 + 5, 8 * (i + 1), 0, bltPos, 0, 16, 8, 0)
        # パドルの描画
        pyxel.blt(self.pad_x, self.pad_y, 0, 40, 0, PAD_W, PAD_H, 0)
        # ボールの描画
        pyxel.blt(self.ball_x, self.ball_y, 0, 0, 8, BALL_W, BALL_H, 0)

        if self.game_state==TITLE:
            pyxel.blt(20,pyxel.height/2-15,1,0,0,200,16,0) 
        elif self.game_state==CLEAR:
            pyxel.blt(30,pyxel.height/2-15,1,0,32,200,16,0) 
        elif self.game_state==OVER:  
            pyxel.blt(20,pyxel.height/2-15,1,0,16,200,16,0) 
        elif self.game_state==MISS:
            pyxel.blt(45,pyxel.height/2-15,1,0,48,200,16,0) 

if __name__ == "__main__":
    App()
