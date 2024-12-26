from django.shortcuts import render
from .models import Candidate
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from .models import Candidate
from .blockchain import cast_vote_on_blockchain, get_candidate_votes

# Create your views here.
def index(request):
    return render(request, 'index.html', {})
def voting(request):
    voting = Candidate.objects.all()
    context = {
        'voting': voting,
    }
    return render(request, 'voting.html',context)
def dashboard(request):
    return render(request, 'dashboard.html', {})


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

def get_results_view(request):
    candidates = Candidate.objects.all()
    results = []

    for candidate in candidates:
        # Get vote count from the blockchain
        votes = get_candidate_votes(candidate.id)
        results.append({
            "candidate_name": candidate.name,
            "votes": votes
        })

    return render(request, "results.html", {"results": results})