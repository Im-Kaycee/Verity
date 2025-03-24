from django.contrib import admin
from .models import Candidate
from .blockchain import sync_candidates_to_blockchain  # Import the sync function

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

    # Adding a custom action to sync candidates to blockchain
    actions = ['sync_candidates_to_blockchain_action']

    def sync_candidates_to_blockchain_action(self, request, queryset):
        """
        Admin action to sync selected candidates to the blockchain.
        """
        # Iterate through the selected candidates and sync each one to the blockchain
        for candidate in queryset:
            # Sync candidate to blockchain
            sync_candidates_to_blockchain(candidate.id, candidate.name)
        
        self.message_user(request, "Candidates have been synced to the blockchain.")

    # Set label for the action
    sync_candidates_to_blockchain_action.short_description = "Sync selected candidates to blockchain"

# Register the model with the updated CandidateAdmin
admin.site.register(Candidate, CandidateAdmin)
