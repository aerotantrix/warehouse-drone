
class Automate:
        
    def move_to_target_location(self) -> None:
        try:
            if self.tello.get_battery() <= 10:
                raise Exception(f'Low Battery: {self.tello.get_battery()}')
            else:
                print(f'Battery: {self.tello.get_battery()}%')
            self.tello.takeoff()
            self.tello.streamon()
            self.tello.move_up(self.column_size*(self.box_height - 1)-40)
        except Exception as e:
            print('Error in move_to_target_location(): ', e)
        
        
        
    def move_to_initial_location(self) -> None:
        if self.row_size % 2 == 0:
            self.tello.land()
        else:
            self.tello.move_left(self.row_size*self.box_height)
            self.tello.land()
    
    
    
    def pattern(self) -> None:
        self.tello.set_speed(20)
        bin_key =0
        for i in range(self.row_size):
            for j in range(self.column_size):
                if i % 2 == 0:
                    self.tello.move_right(self.box_height)
                elif i % 2 != 0:
                    self.tello.move_left(self.box_height)
                time.sleep(self.Sleep_time)
                #rack_key = chr(ord('A') + j)    # Convert ASCII to get 'A', 'B', 'C', ...
                #self.ProductData=self.qr_process(i, j)
                if self.ProductData=="Not available":
                    self.Status=0
                self.Status=1
                self.Dictionary={"BIN ID:":bin_key,
                                 "RACK NO:":j,
                                 "SHELF ":1,
                                 "ProductData":self.ProductData,
                                 "Status":self.Status}
                
                #self.send_data_to_server()
                bin_key +=1   # Bin values starting from 1eft
            if (self.row_size-i) != 1:
                self.tello.move_down(self.box_width)
            else:
                self.move_to_initial_location()