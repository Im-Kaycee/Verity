from django.shortcuts import render
from .models import Candidate
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from .models import Candidate
from .blockchain import cast_vote_on_blockchain, get_candidate_votes
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def index(request):
    return render(request, 'index.html', {})
@login_required
def voting(request):
    voting = Candidate.objects.all()
    context = {
        'voting': voting,
    }
    return render(request, 'voting.html',context)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})
def help_view(request):
    return render(request, 'help.html', {})
@login_required
def cast_vote_view(request):
    if request.method == "POST":
        candidate_id = int(request.POST.get("candidate_id"))
        voter_address = request.user.wallet_address  # Assuming the wallet address is stored for the user

        try:
            cast_vote_on_blockchain(voter_address, candidate_id)
            return JsonResponse({"success": True, "message": "Vote cast successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # Render the page with the list of candidates from the database
    candidates = Candidate.objects.all()
    return render(request, "cast_vote.html", {"candidates": candidates})
@login_required
def get_results_view(request):
    candidates = Candidate.objects.all()
    results = []

    for candidate in candidates:
        try:
            # Get vote count from the blockchain
            votes = get_candidate_votes(candidate.id)
            results.append({
                "candidate_name": candidate.name,
                "votes": votes
            })
        except Exception as e:
            # If there's an error getting votes, log it or handle accordingly
            print(f"Error fetching votes for candidate {candidate.id}: {str(e)}")
            results.append({
                "candidate_name": candidate.name,
                "votes": 0  # Default to 0 if there was an error
            })

    return render(request, "results.html", {"results": results})

# This view will fetch all candidates and their votes and send them to the template.
def is_admin(user):
    return user.is_authenticated and user.is_staff