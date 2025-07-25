import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import Papa from 'papaparse';
import { CommonModule, NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-csv-upload',
  standalone: true,
  imports: [CommonModule, HttpClientModule, NgIf, NgFor],
  templateUrl: './csv-upload.component.html',
  styleUrls: ['./csv-upload.component.css']
})
export class CsvUploadComponent {
  selectedFile: File | null = null;
  csvData: any[] = [];
  columns: string[] = [];

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  uploadFile() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post('http://localhost:5000/csv', formData, { responseType: 'text' })
      .subscribe(response => {
        Papa.parse(response, {
          header: true,
          skipEmptyLines: true,
          complete: (result) => {
            this.csvData = result.data;
            this.columns = result.meta.fields ?? [];
          }
        });
      });
  }
}
