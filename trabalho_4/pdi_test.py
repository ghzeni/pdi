import pdi as pdi

def main():
    image = [ 
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,1,0,0,0,0,0,0,0],
      [0,0,1,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,1,0,0,1,1,0,0],
      [0,0,0,1,0,0,1,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,1,0,0,0,1,0,0,0],
      [0,0,1,0,0,1,1,0,0,0],
      [0,0,1,0,0,0,0,0,0,0] 
      ]

    x = 3
    y = 3
    m=10
    n=10
    replacement_color=2
    print("Original Image: \n")
    for i in range(m):
        for j in range(n):
            print(image[i][j], end=" ")
        print()
    painted = pdi.label_blobs(image)
    
    # Printing the updated screen
    print("\nColored Image: \n")
    for i in range(m):
        for j in range(n):
            print(painted[i][j], end=" ")
        print()

if __name__ == '__main__':
  main ()