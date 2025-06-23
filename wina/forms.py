from django import forms
from .models import Transaction, Booth, Institution


class TransactionForm(forms.ModelForm):
    booth = forms.ModelChoiceField(
        queryset=Booth.objects.all(), empty_label="Select a booth"
    )
    service = forms.ModelChoiceField(
        queryset=Institution.objects.none(), empty_label="Select a service"
    )

    class Meta:
        model = Transaction
        fields = ["booth", "service", "amount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['booth'].label = 'Select Booth'
        self.fields["booth"].widget.attrs["class"] = "text-sky-600 hover:text-white duration-500 bg-white hover:bg-sky-500 focus:ring-4 focus:outline-none focus:ring-sky-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center"

        self.fields['service'].label = 'Select Service'
        self.fields["service"].widget.attrs["class"] = "text-sky-600 hover:text-white duration-500 bg-white hover:bg-sky-500 focus:ring-4 focus:outline-none focus:ring-sky-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center"
        
        self.fields['amount'].label = 'Transaction Amount'
        self.fields["amount"].widget.attrs["class"] = "w-[100%] text-center p-2 rounded-md border border-gray-300"

        # Add placeholder for amount field
        self.fields['amount'].widget.attrs.update({'placeholder': 'Enter amount'})

        if "booth" in self.data:
            try:
                booth_id = int(self.data.get("booth"))
                self.fields["service"].queryset = Booth.objects.get(
                    id=booth_id
                ).services.all()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["service"].queryset = self.instance.booth.services.all()
        
