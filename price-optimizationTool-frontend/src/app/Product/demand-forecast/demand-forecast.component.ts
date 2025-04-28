import { Component, ElementRef, ViewChild, AfterViewInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA,MatDialogRef  } from '@angular/material/dialog';

import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
);

@Component({
  selector: 'app-demand-forecast',
  templateUrl: './demand-forecast.component.html',
  styleUrls: ['./demand-forecast.component.css']
})
export class DemandForecastComponent implements AfterViewInit {

  @ViewChild('forecastChart') chartRef!: ElementRef<HTMLCanvasElement>;
  chart!: Chart;

  forecastData: any[] = [];

  constructor(@Inject(MAT_DIALOG_DATA) public data: any[],  private dialogRef: MatDialogRef<DemandForecastComponent>) {
    // data is an array of selected product objects
    this.forecastData = data || [];
  }

  ngAfterViewInit(): void {
    if (this.chartRef?.nativeElement && this.forecastData.length > 0) {
      this.chart = new Chart(this.chartRef.nativeElement, {
        type: 'line',
        data: {
          labels: this.forecastData.map(d => d.name),
          datasets: [
            {
              label: 'Product Demand',
              data: this.forecastData.map(d => d.demand_forecast),
              borderColor: '#c33fff',
              borderWidth: 2,
              fill: false
            },
            {
              label: 'Selling Price',
              data: this.forecastData.map(d => d.selling_price),
              borderColor: '#00ffc3',
              borderWidth: 2,
              fill: false
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: 'white'
              }
            }
          },
          scales: {
            x: {
              type: 'category',
              ticks: { color: '#fff' },
              grid: { color: '#333' }
            },
            y: {
              ticks: { color: '#fff' },
              grid: { color: '#333' }
            }
          }
        }
      });
    }
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
  
}
