# GAME：太空生存戰
## 介紹
- 2023.01.12 ~ 2023.01.17：以pygame的函式庫製作的一個小遊戲
- 一點小記錄
- pygame docs：https://www.pygame.org/docs/
- 一些參考資料：https://blog.techbridge.cc/2019/10/19/how-to-build-up-game-with-pygame-tutorial/

## 遊戲操作說明
1. 以 **⬅** 跟 **➡** 的方向鍵來控制飛船移動方向
2. 按**space**鍵可以發射飛彈擊破隕石
3. 按"**8**"可以自由開啟或關閉背景音樂
4. 按"**7**"可以自由開啟或關閉音效
5. 若飛船被隕石擊中，則會消耗生命值
6. 飛船有兩條生命值，若**生命值歸零兩次則遊戲結束**
7. 點擊**再來一次**或**space**鍵則可重新開始遊戲
8. 按**ESC**可以手動退出

## 練習筆記
### 遊戲架構
1. 遊戲初始化及創建視窗
2. 遊戲迴圈
    - 讀取使用者輸入
    - 操作更新
    - 顯示螢幕
3. 跳出迴圈：結束遊戲
```
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Game Name")

...(something)...

running = True
while running:
    # get userInput
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ...(something)...

    # show screen
    screen.fill( BACKGROUND ) #RGB
    pygame.display.update()

pygame.quit()
```
### render操作
- 有物件後，可以用`all_sprites`顯示一次顯示在螢幕上
```
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(other_things)

all_sprites.update()

# show on `screen`
all_sprites.draw(screen)
```
### 其他重點func
- 設定FPS
```
FPS = 60
clock = pygame.time.Clock()
while ...:
    clock.tick(FPS)      # 一秒內最多只能被執行n次loop (FPS)
```
- 按鍵輸入操作
```
# get userInput 1
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            player.shoot()
        if event.key == pygame.K_ESCAPE:    #ESC: end the game
            running = False

# get userInput 2
key_pressed = pygame.key.get_pressed()
if key_pressed[pygame.K_RIGHT]:
    self.rect.x += self.speedX
if key_pressed[pygame.K_LEFT]:
    self.rect.x -= self.speedX
```
## 把遊戲py檔轉成可執行檔
### 下載`auto-pt-to-exe`並開啟使用
```
pip install auto-py-to-exe
auto-py-to-exe
```

## 未來計畫
- 看看能否暫停遊戲
- 按鈕文字介面：2023.01.13 & 17完成開頭和結束文字介面，但**因為沒有按鈕物件，所以只有偵測點擊功能**
- 更多飛船skin
- 隕石大小顆：2023.01.13完成