export class Station {
  station_name!: string;
  battery!: number;

  constructor(station_name: string, battery: number) {
    this.station_name = station_name;
    this.battery = battery;
  }
}

export class Bin {
  bin_id!: string;
  timestamp!: Date;
  row!: number;
  rack!: number;
  shelf!: number;
  status!: boolean;

  constructor(
    bin_id: string,
    timestamp: Date,
    row: number,
    rack: number,
    shelf: number,
    status: boolean
  ) {
    this.bin_id = bin_id;
    this.timestamp = timestamp;
    this.row = row;
    this.rack = rack;
    this.shelf = shelf;
    this.status = status;
  }
}

export class GridBin {
  bin_id!: string;
  color!: string;
  
  constructor(bin_id: string, color: string) {
    this.bin_id = bin_id;
    this.color = color;
  }
}
