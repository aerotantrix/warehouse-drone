export class Station {
  stationname!: string;
  battery!: number;

  constructor(stationname: string, battery: number) {
    this.stationname = stationname;
    this.battery = battery;
  }
}

export class Bin {
  bin_id!: string;
  timestamp!: Date;
  row!: number;
  rack!: number;
  shelf!: number;
  present!: boolean;

  constructor(
    bin_id: string,
    timestamp: Date,
    row: number,
    rack: number,
    shelf: number,
    present: boolean
  ) {
    this.bin_id = bin_id;
    this.timestamp = timestamp;
    this.row = row;
    this.rack = rack;
    this.shelf = shelf;
    this.present = present;
  }
}
