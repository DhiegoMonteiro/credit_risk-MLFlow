import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-data-input',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './data-input.component.html',
  styleUrls: ['./data-input.component.css']
})
export class DataInputComponent {
  private fb = inject(FormBuilder);
  private http = inject(HttpClient);
  private router = inject(Router);

  goToCsvUpload() {
    this.router.navigate(['/csv-upload']);
  }
  
  homeOwnershipOptions = [
    { value: 0, label: 'Aluguel' },
    { value: 1, label: 'Propria' },
    { value: 2, label: 'Hipoteca' },
    { value: 3, label: 'Outro' }
  ];

  loanIntentOptions = [
    { value: 0, label: 'Pessoal' },
    { value: 1, label: 'Educação' },
    { value: 2, label: 'Médico' },
    { value: 3, label: 'Empreendimento' },
    { value: 4, label: 'Melhoria da Casa' },
    { value: 5, label: 'Consolidação de Dívidas' }
  ];

  loanGradeOptions = [
    { value: 0, label: 'A' },
    { value: 1, label: 'B' },
    { value: 2, label: 'C' },
    { value: 3, label: 'D' },
    { value: 4, label: 'E' },
    { value: 5, label: 'F' },
    { value: 6, label: 'G' }
  ];

  defaultOnFileOptions = [
    { value: 0, label: 'Não' },
    { value: 1, label: 'Sim' }
  ];

  creditForm: FormGroup = this.fb.group({
    person_age: [25, [Validators.required, Validators.min(18), Validators.max(100)]],
    person_income: [50000, [Validators.required, Validators.min(0)]],
    person_home_ownership: [1, Validators.required],
    person_emp_length: [3, [Validators.required, Validators.min(0)]],
    loan_intent: [2, Validators.required],
    loan_grade: [1, Validators.required],
    loan_amnt: [10000, [Validators.required, Validators.min(0)]],
    loan_int_rate: [12.5, [Validators.required, Validators.min(0), Validators.max(30)]],
    loan_percent_income: [0.2, [Validators.required, Validators.min(0), Validators.max(1)]],
    cb_person_default_on_file: [0, Validators.required],
    cb_person_cred_hist_length: [5, [Validators.required, Validators.min(0)]]
  });

  loading = false;
  errorMessage = '';

  onSubmit() {
    if (this.creditForm.invalid) {
      this.errorMessage = 'Please fill out all required fields correctly.';
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.http.post<any>('http://localhost:5000/predict', this.creditForm.value)
      .subscribe({
        next: (response) => {
          this.loading = false;
          // Navigate to results page with data
          this.router.navigate(['/results'], { 
            state: { 
              formData: this.creditForm.value,
              result: response
            } 
          });
        },
        error: (error) => {
          this.loading = false;
          this.errorMessage = 'Error submitting data: ' + (error.message || 'Unknown error');
          console.error('Prediction error:', error);
        }
      });
  }
}